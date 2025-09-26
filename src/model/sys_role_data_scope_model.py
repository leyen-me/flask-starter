from sqlalchemy import Column, BigInteger

from .base_model import BaseModel


class SysRoleDataScopeModel(BaseModel):
    __tablename__ = "sys_role_data_scope"

    role_id = Column(BigInteger, comment="角色ID")
    org_id = Column(BigInteger, comment="机构ID")
