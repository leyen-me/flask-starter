from db import db

class Result:
    code = 0
    msg = 'success'
    data = None

    """
    处理返回时的序列化问题
    """
    @classmethod
    def handle(cls, data):
        if (str(type(data))=="<class 'NoneType'>"):
            return data
        if (str(type(data))=="<class 'int'>"):
            return data
        if (str(type(data))=="<class 'str'>"):
            return data
        if (str(type(data))=="<class 'bool'>"):
            return data
        if (str(type(data))=="<class 'datetime.datetime'>"):
            return str(data)
        if (str(type(data))=="<class 'bytes'>"):
            return data.decode('utf-8')
        if (str(type(data))=="<class 'dict'>"):
            __dict__ = {}
            for key in data:
                __dict__[key] = cls.handle(data[key])
            return __dict__
        if (str(type(data))=="<class 'list'>"):
            __list__ = []
            for item in data:
                __list__.append(cls.handle(item))
            return __list__
        
        # 处理元组
        if isinstance(data, tuple):
            return cls.handle(list(data))

        # 处理异常类型
        if(isinstance(data, BaseException)):
            return str(data)
        
        # 处理模型
        if(isinstance(data, db.Model)):
            __obj__ = {}
            attributes_and_methods = dir(data)
            attributes = [attr for attr in attributes_and_methods if (not callable(getattr(data, attr)) and not attr.startswith("_") and not attr.endswith("_") and attr != 'metadata' and attr !='query' and attr != 'registry')]
            __obj__ = {}
            for attr in attributes:
                __obj__[attr] = cls.handle(getattr(data, attr))
            return __obj__
        
        # 处理行
        if (str(type(data))=="<class 'sqlalchemy.engine.row.Row'>"):
            return cls.handle(data._asdict())
        
        # 普通对象
        attributes_and_methods = dir(data)
        attributes = [attr for attr in attributes_and_methods if (not callable(getattr(data, attr)) and not attr.startswith("_") and not attr.endswith("_"))]
        __obj__ = {}
        for attr in attributes:
            __obj__[attr] = cls.handle(getattr(data, attr))
        return __obj__

    @classmethod
    def ok(cls, data):
        res = Result()
        res.data = data
        return cls.handle(res)

    @classmethod
    def error(cls, msg):
        res = Result()
        res.code = 500
        res.msg = msg
        return cls.handle(res)