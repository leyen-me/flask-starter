from sqlalchemy import Column, BigInteger

from .base_model import BaseModel


class SysUserRoleModel(BaseModel):
    __tablename__ = "sys_user_role"

    role_id = Column(BigInteger, comment="角色ID")
    user_id = Column(BigInteger, comment="用户ID")
