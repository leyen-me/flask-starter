from sqlalchemy import Column, Integer, String, Column

from .sys_base_model import SysBaseModel


class SysLogLoginModel(SysBaseModel):
    __tablename__ = "sys_log_login"

    username = Column(String(50), comment="用户名")
    ip = Column(String(32), comment="登录IP")
    # address = Column(String(32), comment="登录地点")
    user_agent = Column(String(500), comment="User Agent")
    status = Column(Integer, comment="登录状态  0：失败   1：成功")
    operation = Column(Integer, comment="操作信息   0：登录成功   1：退出成功  2：验证码错误  3：账号密码错误")
