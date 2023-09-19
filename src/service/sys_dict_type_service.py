from flask import request
from sqlalchemy import text

from db import db
from model import SysDictTypeModel, SysDictDataModel
from service import BaseService



class SysDictTypeService(BaseService):

    def page(self):
        # 非必传参数
        dict_type = request.args.get('dict_type')
        dict_name = request.args.get('dict_name')
        query = db.session.query(SysDictTypeModel).filter(SysDictTypeModel.deleted == 0)
        if dict_type:
            query = query.filter(SysDictTypeModel.dict_type.like(f"%{dict_type}%"))
        if dict_name:
            query = query.filter(SysDictTypeModel.dict_name.like(f"%{dict_name}%"))
        return self.query_page(query)
    
    """
    select id as dictValue, name as dictLabel from sys_menu where deleted = 0
    """
    def get_dict_sql(self, id):
        dict_type = db.session.query(SysDictTypeModel).filter(SysDictTypeModel.id == id, SysDictTypeModel.deleted == 0).one()
        try:
            res = db.session().execute(text(dict_type.dict_sql)).fetchall()
            return res
        except:
            raise Exception("动态SQL执行失败，请检查SQL是否正确！")

    def get_dict_list(self):
        type_list = SysDictTypeModel.query.filter_by(deleted=0).all()
        data_list = SysDictDataModel.query.order_by(SysDictDataModel.sort.asc()).filter_by(deleted=0).all()

        for type_item in type_list:
            type_item.data_list = []
            for data_item in data_list:
                if data_item.dict_type_id == type_item.id:
                    type_item.data_list.append(data_item)
            if type_item.dict_source == 1:
                try:
                    res = db.session().execute(text(type_item.dict_sql)).fetchall()
                    type_item.data_list.append(res)
                except:
                    pass
        return type_list

    def save(self, vo):
        dict_type = SysDictTypeModel(**vo)
        db.session.add(dict_type)
        db.session.commit()

    def update(self, vo):
        dict_type = db.session.query(SysDictTypeModel).filter(SysDictTypeModel.id == vo['id'], SysDictTypeModel.deleted == 0).one()
        for key, value in vo.items():
            setattr(dict_type, key, value)
        db.session.commit()

    def delete(self, id_list):
        super().remove_by_ids(id_list)