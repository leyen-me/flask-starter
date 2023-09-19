from sqlalchemy import Column, BigInteger

from db import db
from .sys_base_model import SysBaseModel



class SysRoleDataScopeModel(SysBaseModel, db.Model):
    __tablename__ = "sys_role_data_scope"

    role_id = Column(BigInteger, comment="角色ID")
    org_id = Column(BigInteger, comment="机构ID")