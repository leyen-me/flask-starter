from sqlalchemy import Column, BigInteger

from db import db
from .sys_base_model import SysBaseModel



class SysRoleMenuModel(SysBaseModel, db.Model):
    __tablename__ = "sys_role_menu"

    role_id = Column(BigInteger, comment="角色ID")
    menu_id = Column(BigInteger, comment="菜单ID")