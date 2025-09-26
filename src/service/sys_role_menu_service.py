from db import db
from service import BaseService
from model import SysRoleMenuModel



class SysRoleMenuService(BaseService):

    def save_or_update(self, role_id, menu_id_list):

        # 数据库菜单ID列表
        _db_menu_id_list = db.session.query(SysRoleMenuModel).filter(SysRoleMenuModel.role_id == role_id, SysRoleMenuModel.deleted == 0).all()
        db_menu_id_list = [item.menu_id for item in _db_menu_id_list]

        # 需要新增的菜单ID
        insert_menu_id_list = list(set(menu_id_list) - set(db_menu_id_list))
        for menu_id in insert_menu_id_list:
            db.session.add(SysRoleMenuModel(role_id=role_id, menu_id=menu_id))
        db.session.commit()

        # 需要删除的岗位ID
        delete_menu_id_list = list(set(db_menu_id_list) - set(menu_id_list))
        res = db.session.query(SysRoleMenuModel).filter(SysRoleMenuModel.role_id == role_id,SysRoleMenuModel.menu_id.in_(delete_menu_id_list),SysRoleMenuModel.deleted == 0).all()
        for model in res:
            model.deleted = 1
            db.session.add(model)
        db.session.commit()
    
    def delete_by_role_id_list(self, role_id_list):
        user_role_list = db.session.query(SysRoleMenuModel).filter(SysRoleMenuModel.role_id.in_(role_id_list)).all()
        for user_role in user_role_list:
            user_role.deleted = 1
        db.session.commit()

    def delete_by_menu_id(self, menu_id):
        role_menu_list = db.session.query(SysRoleMenuModel).filter(SysRoleMenuModel.menu_id == menu_id).all()
        for role_menu in role_menu_list:
            role_menu.deleted = 1
        db.session.commit()

    def get_menu_id_list(self, role_id):
        _db_menu_id_list = db.session.query(SysRoleMenuModel).filter(SysRoleMenuModel.role_id == role_id, SysRoleMenuModel.deleted == 0).all()
        db_menu_id_list = [item.menu_id for item in _db_menu_id_list]
        return db_menu_id_list