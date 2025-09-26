from sqlalchemy import Column, Integer, String

from .base_model import BaseModel


class SysParamsModel(BaseModel):
    __tablename__ = "sys_params"

    param_name = Column(String(100), comment="参数名称")
    param_type = Column(Integer, nullable=False, comment="系统参数   0：否   1：是")
    param_key = Column(String(100), comment="参数键")
    param_value = Column(String(2000), comment="参数值")
    remark = Column(String(200), comment="备注")
