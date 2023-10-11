from flask import request

from db import db
from model import SysAttachmentModel
from service import BaseService



class SysAttachmentService(BaseService):

    def page(self):
        # 非必传参数
        name = request.args.get('name')
        platform = request.args.get('platform')
        query = db.session.query(SysAttachmentModel).filter(SysAttachmentModel.deleted == 0)
        if name:
            query = query.filter(SysAttachmentModel.name.like(f"%{name}%"))
        if platform:
            query = query.filter(SysAttachmentModel.platform.like(f"%{platform}%"))
        return self.query_page(query)
    
    def save(self, vo):
        dict_type = SysAttachmentModel(**vo)
        db.session.add(dict_type)
        db.session.commit()

    def delete(self, id_list):
        super().remove_by_ids(id_list)