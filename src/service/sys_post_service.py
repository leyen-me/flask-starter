from flask import request

from db import db
from model import SysPostModel
from service import BaseService, SysUserPostService



class SysPostService(BaseService):

    def page(self):
        query = db.session.query(SysPostModel)

        post_code   = request.args.get('post_code')
        if post_code:
            query = query.filter(SysPostModel.post_code.like(f"%{post_code}%"))

        post_name   = request.args.get('post_name')
        if post_name:
            query = query.filter(SysPostModel.post_name.like(f"%{post_name}%"))

        status      = request.args.get('status')
        if status:
            query = query.filter(SysPostModel.status == status)
        
        query = query.filter(SysPostModel.deleted == 0)
        return self.query_page(query)
    
    def get_list(self):
        res = db.session.query(SysPostModel).filter(SysPostModel.status == 1, SysPostModel.deleted == 0).all()
        return res

    def save(self, vo):
        post = SysPostModel(**vo)
        db.session.add(post)
        db.session.commit()
        return post
    
    def update(self, vo):
        org = db.session.query(SysPostModel).filter(SysPostModel.id==vo['id'], SysPostModel.deleted==0).one()
        for key, value in vo.items():
            setattr(org, key, value)
        db.session.commit()

    def delete(self, id_list):
        #  删除岗位
        posts = db.session.query(SysPostModel).filter(SysPostModel.id.in_(id_list), SysPostModel.deleted == 0).all()
        for post in posts:
            post.deleted = 1
        db.session.commit()
        # 删除岗位用户关系
        SysUserPostService().delete_by_post_id_list(id_list)