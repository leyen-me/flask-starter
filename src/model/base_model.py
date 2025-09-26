from sqlalchemy import Column, BigInteger, Integer, DateTime
from datetime import datetime
from sqlalchemy import event
from flask import g

from db import db


class BaseModel(db.Model):
    __abstract__ = True
    __table_args__ = {'mysql_charset': 'utf8mb4', 'mysql_engine': 'InnoDB'}

    id = Column(BigInteger, primary_key=True, nullable=False, comment="id")
    version = Column(Integer, default=1, comment="版本号")
    deleted = Column(Integer, default=0, comment="删除标识  0：正常   1：已删除")
    creator = Column(BigInteger, comment="创建者")
    updater = Column(BigInteger, comment="更新者")
    create_time = Column(DateTime, default=datetime.now(), comment="创建时间")
    update_time = Column(DateTime, default=datetime.now(), comment="更新时间")


@event.listens_for(BaseModel, "before_insert", propagate=True)
def before_insert_listener(mapper, connection, model):
    model.id = None if not model.id else model.id
    model.creator = g.user["id"] if model.creator is None else model.creator
    model.updater = g.user["id"] if model.updater is None else model.updater


@event.listens_for(BaseModel, 'before_update', propagate=True)
def before_update_listener(mapper, connection, model):
    if isinstance(model.version, int):
        model.version = model.version + 1
    model.updater = g.user["id"]
    model.update_time = datetime.now()
