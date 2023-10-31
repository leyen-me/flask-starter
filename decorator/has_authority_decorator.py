from functools import wraps
from flask import g


def has_authority(auth):
    """
    接口访问权限
    使用方法
        @xxx_controller.route("/xxx", methods=['GET'])
        @has_authority("xxx:xxxx:xxxxx")
        def fun_name():
            pass
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 只有非超级管理员才检查权限
            if auth not in g.user["authority_set"] and g.user['super_admin'] != 1:
                raise Exception("你没有该访问权限")
            return func(*args, **kwargs)

        return wrapper

    return decorator
