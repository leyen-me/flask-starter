from sqlalchemy import Column, BigInteger, String, DateTime

from db import db, db_table_args

class SysUserTokenModel(db.Model):
    __table_args__ = db_table_args  # 由于这个类没有继承 BaseModel，所以需要自行实现
    __tablename__ = "sys_user_token"

    id = Column(BigInteger, primary_key=True, nullable=False, comment="id")
    user_id = Column(BigInteger, comment="用户ID")
    access_token = Column(String(50), nullable=False, comment="token")
    access_token_expire = Column(DateTime, comment="token过期时间")
    create_time = Column(DateTime, comment="创建时间")