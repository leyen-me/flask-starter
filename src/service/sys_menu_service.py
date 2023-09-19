from itertools import chain
from sqlalchemy import text

from db import db
from model import SysMenuModel
from common import Tree, Result
from service import BaseService, SysRoleMenuService



class SysMenuService(BaseService):

    # 获取用户权限标识
    def get_user_authority(self, user):
        
        def format(res):
            # 分割权限标识
            res = [str(r[0]).split(',') for r in res]
            # 转换为列表
            res = list(chain.from_iterable(res))
            # 去除无用的权限标识None和空字符串
            res = [item for item in res if item is item.strip() != 'None' and item.strip() != '']
            return res

        # 判断当前用户是否是超级管理员
        if user['super_admin']:
            res = SysMenuModel.query.with_entities(SysMenuModel.authority).filter(SysMenuModel.deleted==0).all()
            return format(res)
        else:
            sql = text("""select t3.authority from sys_user_role t1 
                       left join sys_role_menu t2 on t1.role_id = t2.role_id 
                       left join sys_menu t3 on t2.menu_id = t3.id
                       where t1.user_id = :user_id and t1.deleted = 0 and t2.deleted = 0 and t3.deleted = 0 
                       order by t3.sort asc""")
            res = db.session().execute(sql, {'user_id': user['id']})
            return format(res.fetchall())

    def get_menu_list(self, menu_type):
        query = db.session.query(SysMenuModel)
        if menu_type != None:
            query.filter(SysMenuModel.type == menu_type)
        menu_list = query.filter(SysMenuModel.deleted == 0).order_by(SysMenuModel.sort.asc()).all()
        menu_list = Result.handle(menu_list)
        return Tree.build_tree(menu_list)

    def get_user_menu_list(self, user, menu_type):
        if user['super_admin']:
            menu_list = self.get_menu_list(menu_type)
        else:
            menu_list = []
        return menu_list

    def info(self, id):
        menu = super().info(id)
        # 获取上级菜单名称
        if not menu.pid == 0:
            parent_menu = super().info(menu.pid)
            menu.parent_name = parent_menu.name
        return menu
    
    def save(self, vo):
        menu = SysMenuModel(**vo)
        db.session.add(menu)
        db.session.commit()

    def update(self, vo):
        menu = db.session.query(SysMenuModel).filter(SysMenuModel.id==vo['id'], SysMenuModel.deleted==0).one()
        # 上级菜单不能为自己
        if vo['id'] == vo['pid']:
            raise Exception("上级机构不能为自身")
        
        for key, value in vo.items():
            setattr(menu, key, value)
        db.session.commit()

    def get_sub_menu_count(self, pid):
        return db.session.query(SysMenuModel).filter(SysMenuModel.pid == pid, SysMenuModel.deleted==0).count()

    def delete(self, menu_id):
        # 判断是否有子菜单或按钮
        count = SysMenuService().get_sub_menu_count(menu_id)
        if count > 0:
            raise Exception("请先删除子菜单")
        
        menu = db.session.query(SysMenuModel).filter(SysMenuModel.id == menu_id, SysMenuModel.deleted == 0).one()
        menu.deleted = 1
        db.session.commit()

        # # 删除角色菜单关系
        SysRoleMenuService().delete_by_menu_id(menu_id)
