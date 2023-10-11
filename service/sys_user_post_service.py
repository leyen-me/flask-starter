from db import db
from service import BaseService
from model import SysUserPostModel



class SysUserPostService(BaseService):
    
    def get_post_id_list(self, user_id):
        res = db.session.query(SysUserPostModel).with_entities(SysUserPostModel.post_id).filter(SysUserPostModel.user_id == user_id).filter(SysUserPostModel.deleted == 0).all()
        role_id_List = [item[0] for item in res]
        return role_id_List
    
    def delete_by_post_id_list(self, id_list):
        posts = db.session.query(SysUserPostModel).filter(SysUserPostModel.post_id.in_(id_list)).all()
        for post in posts:
            post.deleted = 1
        db.session.commit()
        return True
    
    def delete_by_user_id_list(self, id_list):
        posts = db.session.query(SysUserPostModel).filter(SysUserPostModel.user_id.in_(id_list)).all()
        for post in posts:
            post.deleted = 1
        db.session.commit()
        return True

    def save_or_update(self, user_id, post_id_list):
        db_post_id_list = self.get_post_id_list(user_id)

        # 需要新增的岗位ID
        insert_post_id_list = list(set(post_id_list) - set(db_post_id_list))
        for post_id in insert_post_id_list:
            db.session.add(SysUserPostModel(user_id=user_id,post_id = post_id))
        db.session.commit()
        
        # 需要删除的岗位ID
        delete_post_id_list = list(set(db_post_id_list) - set(post_id_list))
        res = db.session.query(SysUserPostModel).filter(SysUserPostModel.user_id == user_id,SysUserPostModel.post_id.in_(delete_post_id_list),SysUserPostModel.deleted == 0).all()
        for model in res:
            model.deleted = 1
            db.session.add(model)
        db.session.commit()