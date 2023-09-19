from functools import wraps
from flask import g

def has_authority(auth):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if auth in g.user["authority_set"]:
                return func(*args, **kwargs)
            else:
                raise Exception("你没有该访问权限")
        return wrapper
    return decorator