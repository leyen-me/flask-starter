import json
from schedule import scheduler
from db import redis
from service import SysDictTypeService
from common import Result, RedisKeys


class DictSchedule:

    @classmethod
    def run(cls):
        with scheduler.app.app_context():
            dict_list = SysDictTypeService().get_dict_list()
            redis.set(RedisKeys.get_dict_key(), json.dumps(Result.handle(dict_list)))
