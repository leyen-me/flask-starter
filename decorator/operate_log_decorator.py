from functools import wraps
from flask import g
from service import SysLogOperateService
import time

def operate_log(type):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            try:
                result = func(*args, **kwargs)
                status = 1
            except Exception as e:
                result = str(e)
                status = 0
                raise Exception(result)
            finally:
                end_time = time.time()
                duration = int((end_time - start_time) * 1000)
                data = {
                    "operate_type": type.value,
                    "duration":duration,
                    "user_id": g.user['id'],
                    "real_name": g.user['real_name'],
                    "result_msg": str(result),
                    "status": status
                }
                SysLogOperateService().save(data)
            return result
        return wrapper
    return decorator