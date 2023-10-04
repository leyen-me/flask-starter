from flask import request

from db import db
from model import SysRoleModel
from enums import SysDataScopeEnum
from service import BaseService, SysRoleMenuService, SysUserRoleService, SysRoleDataScopeService



class SysRoleService(BaseService):

    # 不同的数据权限查询到的角色不一样
    def page(self):
        query = db.session.query(SysRoleModel)
        # 非必传参数
        name   = request.args.get('name')
        if name:
            query = query.filter(SysRoleModel.name.like(f"%{name}%"))
        query = query.filter(SysRoleModel.deleted == 0)
        return self.query_page(self.get_query_by_data_scope(query))
    
    def get_list(self):
        query = db.session.query(SysRoleModel)
        query = self.get_query_by_data_scope(query)
        return query.filter(SysRoleModel.deleted == 0).all()
    
    def info(self, role_id):
        return db.session.query(SysRoleModel).filter(SysRoleModel.id == role_id,SysRoleModel.deleted == 0).one()

    def save(self, vo):
        # 保存角色
        role = SysRoleModel(**vo)
        role.data_scope = SysDataScopeEnum.SELF.value
        db.session.add(role)
        db.session.commit()

        # 保存角色菜单关系
        SysRoleMenuService().save_or_update(role.id, vo['menu_id_list'])
        return role

    def update(self, vo):
        # 更新角色
        role = db.session.query(SysRoleModel).filter(SysRoleModel.id == vo['id'],SysRoleModel.deleted == 0).one()
        for key, value in vo.items():
            setattr(role, key, value)
        db.session.commit()
        
        # 更新角色菜单关系
        SysRoleMenuService().save_or_update(role.id, vo['menu_id_list'])

    # 给角色分配数据范围
    def data_scope(self, vo):
         # 更新角色
        role = db.session.query(SysRoleModel).filter(SysRoleModel.id == vo['id'], SysRoleModel.deleted == 0).one()
        role.data_scope = vo['data_scope']
        db.session.commit()

        # 更新角色数据权限关系
        if vo['data_scope'] == SysDataScopeEnum.CUSTOM.value:
            SysRoleDataScopeService().save_or_update(vo['id'], vo['org_id_list'])
        else:
            SysRoleDataScopeService().delete_by_role_id_list([vo['id']])
        
    def delete(self, id_list):
        # 删除角色
        self.remove_by_ids(id_list)
        # 删除用户角色关系
        SysUserRoleService().delete_by_role_id_list(id_list)
        # 删除角色菜单关系
        SysRoleMenuService().delete_by_role_id_list(id_list)
        # 删除角色数据权限关系
        SysRoleDataScopeService().delete_by_role_id_list(id_list)