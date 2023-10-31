from sqlalchemy import Column, BigInteger

from .sys_base_model import SysBaseModel


class SysUserRoleModel(SysBaseModel):
    __tablename__ = "sys_user_role"

    role_id = Column(BigInteger, comment="角色ID")
    user_id = Column(BigInteger, comment="用户ID")
