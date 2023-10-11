from sqlalchemy import Column, Integer, String

from db import db
from .sys_base_model import SysBaseModel



class SysPostModel(SysBaseModel, db.Model):
    __tablename__ = "sys_post"

    post_code = Column(String(100), comment="岗位编码")
    post_name = Column(String(100), comment="岗位名称")
    sort = Column(Integer, comment="排序")
    status = Column(Integer, default=1, comment="状态  0：停用   1：正常")