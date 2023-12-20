from datetime import datetime
from sqlalchemy.engine.row import Row

from logger import logger
from db import db


class Result:
    code = 0
    msg = 'success'
    data = None

    @classmethod
    def serialize(cls, data):
        """
        处理返回时的序列化问题
        """
        # 序列化数据库模型
        # 在构建数据库模型的时候，严禁使用metadata，query，registry属性
        if isinstance(data, db.Model):
            attributes_and_methods = dir(data)
            attributes = [attr for attr in attributes_and_methods if (
                    not callable(getattr(data, attr)) and not attr.startswith("_") and not attr.endswith(
                "_") and attr != 'metadata' and attr != 'query' and attr != 'registry')]
            __obj__ = {}
            for attr in attributes:
                __obj__[attr] = cls.serialize(getattr(data, attr))
            return __obj__
        elif data is None:
            return data
        elif (isinstance(data, int)
              or isinstance(data, str)
              or isinstance(data, bool)
              or isinstance(data, float)):
            return data
        elif isinstance(data, datetime):
            return str(data)
        elif isinstance(data, bytes):
            return data.decode('utf-8')
        elif isinstance(data, dict):
            __dict__ = {}
            for key in data:
                __dict__[key] = cls.serialize(data[key])
            return __dict__
        elif isinstance(data, list):
            __list__ = []
            for item in data:
                __list__.append(cls.serialize(item))
            return __list__
        elif isinstance(data, tuple):
            return cls.serialize(list(data))
        elif isinstance(data, BaseException):
            return str(data)
        elif isinstance(data, Row):
            return cls.serialize(data._asdict())
        elif isinstance(data, object):
            attributes_and_methods = dir(data)
            attributes = [attr for attr in attributes_and_methods if
                          (not callable(getattr(data, attr)) and not attr.startswith("_") and not attr.endswith(
                              "_"))]
            __obj__ = {}
            for attr in attributes:
                __obj__[attr] = cls.serialize(getattr(data, attr))
            return __obj__

    @classmethod
    def handle(cls, data):
        try:
            return cls.serialize(data)
        except Exception as e:
            error_msg = "序列化异常, 请手动添加规则" + ' ' + str(e)
            logger.error(f'{error_msg}')
            raise Exception("序列化异常, 请手动添加规则")

    @classmethod
    def ok(cls, data=None):
        res = Result()
        res.data = data
        return cls.handle(res)

    @classmethod
    def error(cls, msg):
        res = Result()
        res.code = 500
        res.msg = msg
        return cls.handle(res)
