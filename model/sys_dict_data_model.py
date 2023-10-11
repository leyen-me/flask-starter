from sqlalchemy import Column, BigInteger, Integer, String

from db import db
from .sys_base_model import SysBaseModel


class SysDictDataModel(SysBaseModel, db.Model):
    __tablename__ = "sys_dict_data"
    
    dict_type_id = Column(BigInteger, nullable=False, comment="字典类型ID")
    dict_label = Column(String(255), comment="字典标签")
    dict_value = Column(String(255), comment="字典值")
    label_class = Column(String(100), comment="标签样式")
    remark = Column(String(255), comment="备注")
    sort = Column(Integer, default = 0, comment="排序")