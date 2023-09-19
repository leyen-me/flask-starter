from db import db
from service import BaseService
from model import SysRoleDataScopeModel, SysUserRoleModel


class SysRoleDataScopeService(BaseService):

    def save_or_update(self, role_id, org_id_list):
        db_org_list = db.session.query(SysRoleDataScopeModel).filter(SysRoleDataScopeModel.role_id == role_id, SysRoleDataScopeModel.deleted == 0).all()
        db_org_id_list = [item.org_id for item in db_org_list]

        # 需要新增的机构ID
        insert_org_id_list = list(set(org_id_list) - set(db_org_id_list))
        for org_id in insert_org_id_list:
            db.session.add(SysRoleDataScopeModel(org_id = org_id, role_id = role_id))

        # 需要删除的机构ID
        delete_org_id_list = list(set(db_org_id_list) - set(org_id_list))
        res = db.session.query(SysRoleDataScopeModel).filter(SysRoleDataScopeModel.role_id == role_id,SysRoleDataScopeModel.org_id.in_(delete_org_id_list), SysRoleDataScopeModel.deleted == 0).all()
        for model in res:
            model.deleted = 1
            db.session.add(model)

        db.session.commit()

    def delete_by_role_id_list(self, role_id_list):
        user_role_list = db.session.query(SysRoleDataScopeModel).filter(SysRoleDataScopeModel.role_id.in_(role_id_list)).all()
        for user_role in user_role_list:
            user_role.deleted = 1
        db.session.commit()

    def get_org_id_list(self, role_id):
        db_org_list = db.session.query(SysRoleDataScopeModel).filter(SysRoleDataScopeModel.role_id == role_id, SysRoleDataScopeModel.deleted == 0).all()
        db_org_id_list = [item.org_id for item in db_org_list]
        return db_org_id_list
    
    def get_data_scope_list(self, user_id):
        res = db.session.query(SysRoleDataScopeModel.org_id).\
            join(SysUserRoleModel, SysUserRoleModel.role_id == SysRoleDataScopeModel.role_id).\
            filter(SysUserRoleModel.user_id == user_id, SysUserRoleModel.deleted == 0, SysRoleDataScopeModel.deleted == 0).\
            all()
        org_ids = [row.org_id for row in res]
        return org_ids