from sqlalchemy import Column, Integer, String, Column

from .base_model import BaseModel


class SysDictTypeModel(BaseModel):
    __tablename__ = "sys_dict_type"
    
    dict_type = Column(String(100), nullable=False, comment="字典类型")
    dict_name = Column(String(255), nullable=False, comment="字典名称")
    dict_source = Column(Integer, default=0, comment="来源  0：字典数据  1：动态SQL")
    dict_sql = Column(String(500), comment="动态SQL")
    remark = Column(String(255), comment="备注")
    sort = Column(Integer, default=0, comment="排序")