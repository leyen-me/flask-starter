from sqlalchemy import Column, BigInteger

from .sys_base_model import SysBaseModel


class SysUserPostModel(SysBaseModel):
    __tablename__ = "sys_user_post"

    user_id = Column(BigInteger, comment="用户ID")
    post_id = Column(BigInteger, comment="岗位ID")
