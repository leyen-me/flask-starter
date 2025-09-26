import json
from flask import request
from datetime import datetime

from db import db, redis
from model import SysUserTokenModel
from service import BaseService, SysUserDetailsService
from common import RedisKeys, Result


class SysUserTokenService(BaseService):

    # 用户登录成功之后，将token和id存储到数据库进行管理
    def save(self, model):
        db.session.add(model)
        db.session.commit()

    def get_online_access_token_list_by_user_id(self, user_id):
        return db.session.query(SysUserTokenModel).filter(SysUserTokenModel.user_id == user_id, SysUserTokenModel.access_token_expire >= datetime.now()).all()

    def update_cache_auth_by_user_id(self, user_id):
        user_list = self.get_online_access_token_list_by_user_id(user_id)
        for user in user_list:
            self.update_cache_auth(user.access_token)
    
    def update_cache_auth(self, access_token):
        user = redis.get(RedisKeys.get_access_token_key(access_token))
        _user = json.loads(user)
        # 用户不存在
        if user is None:
            return
        # 查询过期时间
        t = redis.ttl(RedisKeys.get_access_token_key(access_token))
        if t <= 0:
            return
        userinfo = SysUserDetailsService().get_user_details(_user['id'])
        userinfo = json.dumps(Result.handle(userinfo))
        redis.set(RedisKeys.get_access_token_key(access_token), userinfo, t)