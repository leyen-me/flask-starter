from db import db
from model import SysUserModel
from common import Result

class SysUserDetailsService():

    #  获取 UserDetails 对象，设置用户权限信息
    def get_user_details(self, user_id):
        from service import SysMenuService, SysUserService
        user = db.session.query(SysUserModel).filter(SysUserModel.id == user_id, SysUserModel.deleted == 0).one()
        # 5.查询User的权限列表
        user.authority_set = SysMenuService().get_user_authority(Result.handle(user))
        # 6.查询这个人的数据范围
        user.data_scope_list = SysUserService().get_data_scope(user)
        return user