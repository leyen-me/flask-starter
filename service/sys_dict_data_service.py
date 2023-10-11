from db import db
from model import SysDictDataModel
from service import BaseService



class SysDictDataService(BaseService):

    def page(self, dict_type_id):
        query = db.session.query(SysDictDataModel).filter(SysDictDataModel.dict_type_id == dict_type_id, SysDictDataModel.deleted == 0)
        return self.query_page(query)
    
    def save(self, vo):
        dict_type = SysDictDataModel(**vo)
        db.session.add(dict_type)
        db.session.commit()

    def update(self, vo):
        dict_type = db.session.query(SysDictDataModel).filter(SysDictDataModel.id == vo['id'], SysDictDataModel.deleted == 0).one()
        for key, value in vo.items():
            setattr(dict_type, key, value)
        db.session.commit()

    def delete(self, id_list):
        super().remove_by_ids(id_list)