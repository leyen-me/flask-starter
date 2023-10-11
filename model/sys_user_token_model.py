from sqlalchemy import Column, BigInteger, String, DateTime

from db import db

class SysUserTokenModel(db.Model):
    __table_args__ = {'mysql_charset': 'utf8mb4', 'mysql_engine': 'InnoDB'}
    __tablename__ = "sys_user_token"

    id = Column(BigInteger, primary_key=True, nullable=False, comment="id")
    user_id = Column(BigInteger, comment="用户ID")
    access_token = Column(String(50), nullable=False, comment="token")
    access_token_expire = Column(DateTime, comment="token过期时间")
    create_time = Column(DateTime, comment="创建时间")