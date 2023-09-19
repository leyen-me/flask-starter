from sqlalchemy import Column, BigInteger, Integer, String

from db import db
from .sys_base_model import SysBaseModel



class SysOrgModel(SysBaseModel, db.Model):
    __tablename__ = "sys_org"

    pid = Column(BigInteger, comment="上级ID")
    name = Column(String(50), comment="机构名称")
    sort = Column(Integer, default=1, comment="排序")

    parent_name = ''

