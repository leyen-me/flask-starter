from sqlalchemy import Column, BigInteger

from .sys_base_model import SysBaseModel


class SysRoleDataScopeModel(SysBaseModel):
    __tablename__ = "sys_role_data_scope"

    role_id = Column(BigInteger, comment="角色ID")
    org_id = Column(BigInteger, comment="机构ID")
