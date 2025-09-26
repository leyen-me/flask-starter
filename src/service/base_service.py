import os
import uuid
import json
import bcrypt
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
    def export(self, trans_dic=None):
        """
        导出
        trans_dic用来指定导出的时候，哪些使用指定的字典
        """
        if trans_dic is None:
            trans_dic = {}

        file_folder = os.path.join(CONFIG['APP']['STATIC_FOLDER'])
        file_name = str(uuid.uuid4()) + ".xlsx"
        file_path = os.path.join(os.getcwd(), file_folder, file_name)

        # 字段列表
        fields = self.model_class.__table__.columns.keys()

        # 字段备注
        fields_desc = {}

        data_dict = []

        for key in fields:
            desc = getattr(self.model_class.__table__.columns[key], 'comment', key) or ''
            fields_desc[key] = desc
        data_dict.append(fields_desc)

        res = db.session.query(self.model_class).all()
        for model in res:
            model_dict = {}
            for key in fields:
                if trans_dic.get(key) is None:
                    model_dict[key] = model.__getattribute__(key)
                else:
                    model_dict[key] = self.get_dict_label(trans_dic.get(key), model.__getattribute__(key))
            data_dict.append(model_dict)

        df = pd.DataFrame(data_dict)
        df.to_excel(file_path, index=False)

        response = make_response(send_file(file_path, as_attachment=True))
        response.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'
        return response
