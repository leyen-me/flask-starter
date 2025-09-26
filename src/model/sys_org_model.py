from sqlalchemy import Column, BigInteger, Integer, String

from .base_model import BaseModel


class SysOrgModel(BaseModel):
    __tablename__ = "sys_org"

    pid = Column(BigInteger, comment="上级ID")
    name = Column(String(50), comment="机构名称")
    sort = Column(Integer, default=1, comment="排序")

    parent_name = ''
