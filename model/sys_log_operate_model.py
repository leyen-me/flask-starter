from sqlalchemy import Column, BigInteger, Integer, String, Text

from db import db
from .sys_base_model import SysBaseModel



# 操作日志表
class SysLogOperateModel(SysBaseModel, db.Model):
    __tablename__ = "sys_log_operate"
    
    # module = Column(String(100), comment="模块名")
    # name = Column(String(100), comment="操作名")
    # address = Column(String(32), comment="登录地点")

    req_uri = Column(String(500), comment="请求URI")
    req_method = Column(String(20), comment="请求方法")
    req_params = Column(Text, comment="请求参数")
    ip = Column(String(32), comment="操作IP")
    user_agent = Column(String(500), comment="User Agent")
    operate_type = Column(Integer, comment="操作类型")
    duration = Column(Integer, comment="执行时长")
    status = Column(Integer, comment="操作状态  0：失败   1：成功")
    user_id = Column(BigInteger, comment="用户ID")
    real_name = Column(String(50), comment="操作人")
    result_msg = Column(Text, comment="返回消息")