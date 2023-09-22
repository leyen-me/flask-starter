from sqlalchemy import Column, BigInteger, Integer, String

from db import db
from .sys_base_model import SysBaseModel



class SysUserModel(SysBaseModel, db.Model):
    __tablename__ = "sys_user"
    username = Column(String(50), nullable=False, comment="用户名")
    password = Column(String(100), comment="密码")
    real_name = Column(String(50), comment="姓名")
    avatar = Column(String(200), comment="头像")
    gender = Column(Integer, comment="性别   0：男   1：女   2：未知")
    email = Column(String(100), comment="邮箱")
    mobile = Column(String(20), comment="手机号")
    org_id = Column(BigInteger, comment="机构ID")
    super_admin = Column(Integer, comment="超级管理员")
    status = Column(Integer, comment="状态")

    role_id_list = []
    post_id_list = []
    data_scope_list = []