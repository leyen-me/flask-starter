from sqlalchemy import Column, BigInteger, Integer, String

from .base_model import BaseModel


class SysUserModel(BaseModel):
    __tablename__ = "sys_user"

    username = Column(String(50), nullable=False, comment="用户名")
    password = Column(String(100), comment="密码")
    real_name = Column(String(50), comment="姓名")
    avatar = Column(String(200), comment="头像")
    gender = Column(Integer, comment="性别   0：男   1：女   2：未知")
    email = Column(String(100), comment="邮箱")
    mobile = Column(String(20), comment="手机号")
    org_id = Column(BigInteger, comment="机构ID")
    super_admin = Column(Integer, default=0, comment="超级管理员")
    status = Column(Integer, default=1, comment="状态")

    # 扩展属性
    authority_set = []
    role_id_list = []
    post_id_list = []
    data_scope_list = []
