from sqlalchemy import Column, BigInteger

from .base_model import BaseModel


class SysUserPostModel(BaseModel):
    __tablename__ = "sys_user_post"

    user_id = Column(BigInteger, comment="用户ID")
    post_id = Column(BigInteger, comment="岗位ID")
