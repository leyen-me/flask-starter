from io import BytesIO
import os
import uuid
import json
import bcrypt
from urllib.parse import quote
from flask import request, g, make_response, send_file
import pandas as pd
from sqlalchemy import or_
from sqlalchemy.orm import Query

from db import db, redis
from common import Result, RedisKeys
from config import CONFIG


class BaseService:
    
    def __init__(self) -> None:
        model_class_name = self.__class__.__name__
        model_class_name = model_class_name.replace("Service", "Model")
        self.model_class = getattr(__import__("model"), model_class_name)

    def query_page(self, query: Query):
        # page -> order asc
        asc = request.args.get('asc')
        order_field = request.args.get('order')
        if order_field:
            field = getattr(self.model_class, order_field)
            if asc:
                query = query.order_by(field.asc() if asc else field.desc())
        
        # page -> page limit
        data = query.paginate(page=int(request.args.get('page')), per_page=int(request.args.get('limit')), error_out=False)
        return { "total": data.total, "list": data.items }

    # 数据权限范围
    def get_query_by_data_scope(self, query, model=None, attr='org_id'):
        _m = self.model_class
        if model:
            _m = model
        # 全部数据权限
        if g.user['super_admin'] or g.user["data_scope_list"] == None:
            return query
        # 数据过滤
        elif len(g.user["data_scope_list"]) > 0:
            query = query.filter(or_(getattr(_m, attr).in_(g.user['data_scope_list']), _m.creator == g.user['id']))
        # 查询本人数据
        else:
            query = query.filter(_m.creator == g.user['id'])
        return query

    # 查询详细信息
    def info(self, id):
        return db.session.query(self.model_class).filter(self.model_class.id == id, self.model_class.deleted == 0).one()

    # 批量删除
    def remove_by_ids(self, id_list):
        data = db.session.query(self.model_class).filter(self.model_class.id.in_(id_list),
                                                         self.model_class.deleted == 0).all()
        for item in data:
            item.deleted = 1
        db.session.commit()
        return data

    @classmethod
    def get_dict_value(cls, dict_type, dict_label):
        cache_dict = json.loads(redis.get(RedisKeys.get_dict_key()))
        for item in cache_dict:
            if item['dict_type'] == dict_type:
                for item2 in item['data_list']:
                    if item2['dict_label'] == str(dict_label):
                        return item2['dict_value']
        return "#字典异常"

    @classmethod
    def get_dict_label(cls, dict_type, dict_value):
        cache_dict = json.loads(redis.get(RedisKeys.get_dict_key()))
        for item in cache_dict:
            if item['dict_type'] == dict_type:
                for item2 in item['data_list']:
                    if item2['dict_value'] == str(dict_value):
                        return item2['dict_label']
                    print(item2)
        return "#字典异常"

    def import_by_excel(self, trans_dic=None):
        """
        默认第一行是数据库字段名
        默认第二行是数据库字段名对应的注释
        """
        if trans_dic is None:
            trans_dic = {}

        if 'file' in request.files:
            file = request.files['file']
            file_name = str(uuid.uuid4()) + os.path.splitext(file.filename)[-1]
            file_folder = os.path.join(CONFIG['APP']['STATIC_FOLDER'])
            file_path = os.path.join(os.getcwd(), file_folder, file_name)
            file.save(file_path)

            df = pd.read_excel(file_path)
            fields = self.model_class.__table__.columns.keys()
            models = []
            for index, row in df.iterrows():
                if index > 0:
                    model_dict = {}
                    for key in fields:
                        try:
                            value = row[key]
                            if key == 'password' and value != None:
                                value = bcrypt.hashpw(password=str(value).encode('utf-8'),
                                                      salt=bcrypt.gensalt()).decode("utf-8")
                        except:
                            value = None
                        if trans_dic.get(key) is None:
                            model_dict[key] = value
                        else:
                            model_dict[key] = self.get_dict_value(trans_dic.get(key), value)

                    models.append(self.model_class(**model_dict))
            db.session.bulk_save_objects(models)
            db.session.commit()

        # 导出
    def export(self, trans_dic=None, filename="export_data"):
        """
        导出数据到Excel，表头仅使用字段的 comment
        :param trans_dic: 字段转换规则字典
        :param filename: 导出文件名（不带扩展名）
        :return: Flask响应对象
        """
        if trans_dic is None:
            trans_dic = {}

        # 1. 获取所有字段，并过滤掉无 comment 或 export=False 的字段
        fields = []
        headers = []  # 存储表头（comment）
        for column in self.model_class.__table__.columns:
            # 检查是否导出（默认导出，除非显式设置 export=False）
            if hasattr(column, "info") and column.info.get("export", True) is False:
                continue
            # 获取 comment，如果不存在则跳过该字段
            comment = getattr(column, "comment", None)
            if not comment:
                continue
            fields.append(column.name)
            headers.append(comment)

        # 2. 查询数据并构建数据字典（表头为 comment）
        data = []
        res = db.session.query(self.model_class).all()
        for model in res:
            row = {}
            for i, key in enumerate(fields):
                # 使用 headers[i]（comment）作为键，保证表头和数据对齐
                if trans_dic.get(key) is None:
                    row[headers[i]] = model.__getattribute__(key)
                else:
                    row[headers[i]] = self.get_dict_label(trans_dic.get(key), model.__getattribute__(key))
            data.append(row)

        # 3. 创建 DataFrame（表头是 headers）
        df = pd.DataFrame(data)

        # 4. 生成 Excel 响应
        output = BytesIO()
        with pd.ExcelWriter(output, engine="openpyxl") as writer:
            df.to_excel(writer, index=False)
        output.seek(0)

        encoded_filename = quote(f"{filename}.xlsx")
        response = make_response(output.getvalue())
        response.headers["Content-Type"] = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        response.headers["Content-Disposition"] = f"attachment; filename*=utf-8''{encoded_filename}"
        response.headers["Access-Control-Expose-Headers"] = "Content-Disposition"
        return response