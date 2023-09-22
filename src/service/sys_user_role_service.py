from db import db
from service import BaseService, SysUserTokenService
from model import SysUserRoleModel



class SysUserRoleService(BaseService):
    
    def get_user_id_list(self, role_id):
        res = db.session.query(SysUserRoleModel).with_entities(SysUserRoleModel.user_id).filter(SysUserRoleModel.role_id == role_id).filter(SysUserRoleModel.deleted == 0).all()
        user_id_list = [item[0] for item in res]
        return user_id_list

    def get_role_id_list(self, user_id):
        res = db.session.query(SysUserRoleModel).with_entities(SysUserRoleModel.role_id).filter(SysUserRoleModel.user_id == user_id).filter(SysUserRoleModel.deleted == 0).all()
        role_id_list = [item[0] for item in res]
        return role_id_list
    
    def delete_by_role_id_list(self, role_id_list):
        user_role_list = db.session.query(SysUserRoleModel).filter(SysUserRoleModel.role_id.in_(role_id_list)).all()
        for user_role in user_role_list:
            user_role.deleted = 1
        db.session.commit()
    
    def delete_by_user_id_list(self, id_list):
        posts = db.session.query(SysUserRoleModel).filter(SysUserRoleModel.user_id.in_(id_list)).all()
        for post in posts:
            post.deleted = 1
        db.session.commit()
        return True
    
    def delete_by_role_id_user_id_list(self, role_id, user_id_list):
        user_role_list = db.session.query(SysUserRoleModel).filter(SysUserRoleModel.role_id == role_id,SysUserRoleModel.user_id.in_(user_id_list)).all()
        for user_role in user_role_list:
            user_role.deleted = 1
        db.session.commit()

        for user_role in user_role_list:
            SysUserTokenService().update_cache_auth_by_user_id(user_role.user_id)

    def save_user_list(self, role_id, user_id_list):
        db_role_id_list = self.get_user_id_list(role_id)
        # 需要新增的用户ID
        insert_user_id_list = list(set(user_id_list) - set(db_role_id_list))
        for user_id in insert_user_id_list:
            db.session.add(SysUserRoleModel(user_id=user_id,role_id = role_id))
        db.session.commit()

        for user_id in insert_user_id_list:
            SysUserTokenService().update_cache_auth_by_user_id(user_id)
  
    def save_or_update(self, user_id, role_id_list):
        db_role_id_list = self.get_role_id_list(user_id)

        # 需要新增的角色ID
        insert_role_id_list = list(set(role_id_list) - set(db_role_id_list))
        for role_id in insert_role_id_list:
            db.session.add(SysUserRoleModel(user_id=user_id,role_id = role_id))

        # 需要删除的角色ID
        delete_role_id_list = list(set(db_role_id_list) - set(role_id_list))
        res = db.session.query(SysUserRoleModel).filter(SysUserRoleModel.user_id == user_id,SysUserRoleModel.role_id.in_(delete_role_id_list),SysUserRoleModel.deleted == 0).all()
        for model in res:
            model.deleted = 1
            db.session.add(model)
        
        db.session.commit()