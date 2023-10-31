from sqlalchemy import Column, BigInteger

from .sys_base_model import SysBaseModel


class SysRoleMenuModel(SysBaseModel):
    __tablename__ = "sys_role_menu"

    role_id = Column(BigInteger, comment="角色ID")
    menu_id = Column(BigInteger, comment="菜单ID")
