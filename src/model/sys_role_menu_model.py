from sqlalchemy import Column, BigInteger

from .base_model import BaseModel


class SysRoleMenuModel(BaseModel):
    __tablename__ = "sys_role_menu"

    role_id = Column(BigInteger, comment="角色ID")
    menu_id = Column(BigInteger, comment="菜单ID")
