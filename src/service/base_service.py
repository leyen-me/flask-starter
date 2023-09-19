import os
import uuid
from flask import request, g
import pandas as pd
from sqlalchemy import or_

from db import db
from common import Result
from config import CONFIG



class BaseService:
    
    def __init__(self) -> None:
        model_class_name = self.__class__.__name__
        model_class_name = model_class_name.replace("Service", "Model")
        self.model_class = getattr(__import__("model"), model_class_name)

    def query_page(self, query):
         # 必传参数
        page     = int(request.args.get('page')) 
        limit    = int(request.args.get('limit'))
        order    = request.args.get('order')
        asc      = request.args.get('asc')
        if order:
            try:
                field = getattr(self.model_class, order)
                if asc:
                    query = query.order_by(field.asc())
                else:
                    query = query.order_by(field.desc())
            except Exception as e:
                raise Exception("缺少参数->" + str(e))
            
        data = query.paginate(page=page, per_page=limit, error_out=False)
        
        return Result.handle({
            "total": data.total,
            "list": data.items
        })
    
    # 数据权限范围
    def get_query_by_data_scope(self, query, model = None, attr = 'org_id'):
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
    def info(self ,id):
        return db.session.query(self.model_class).filter(self.model_class.id == id, self.model_class.deleted == 0).one()
    
    # 批量删除
    def remove_by_ids(self, id_list):
        data = db.session.query(self.model_class).filter(self.model_class.id.in_(id_list), self.model_class.deleted == 0).all()
        for item in data:
            item.deleted = 1
        db.session.commit()
        return data

    # 导出
    def export(self):
        file_folder = os.path.join(CONFIG['APP']['STATIC_FOLDER'])
        file_name = str(uuid.uuid4()) + ".xlsx"
        file_path = os.path.join(os.getcwd(), file_folder +"\\"+file_name)

        fields = self.model_class.__table__.columns.keys()
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
                model_dict[key] = model.__getattribute__(key)
            data_dict.append(model_dict)

        df = pd.DataFrame(data_dict)
        df.to_excel(file_path, index=False)
        return file_path