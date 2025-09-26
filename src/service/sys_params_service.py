from flask import request

from common import RedisKeys
from model import SysParamsModel
from service import BaseService
from db import db, redis



class SysParamsService(BaseService):

    def page(self):
        # 非必传参数
        param_key = request.args.get('param_key')
        param_value = request.args.get('param_value')
        param_type = request.args.get('param_type')
        query = db.session.query(SysParamsModel).filter(SysParamsModel.deleted == 0)
        if param_key:
            query = query.filter(SysParamsModel.param_key.like(f"%{param_key}%"))
        if param_value:
            query = query.filter(SysParamsModel.param_value == param_value)
        if param_type:
            query = query.filter(SysParamsModel.param_type == param_type)
        return self.query_page(query)
    
    def save(self, vo):
        res = db.session.query(SysParamsModel).filter(SysParamsModel.param_key == vo['param_key'], SysParamsModel.deleted == 0).one_or_none()
        if res:
            raise Exception("参数键已存在")
        param = SysParamsModel(**vo)
        db.session.add(param)
        db.session.commit()
        # 保存到缓存
        redis.hset(RedisKeys.get_param_key(), param.param_key, param.param_value)

    def update(self, vo):
        param = db.session.query(SysParamsModel).filter(SysParamsModel.id == vo['id'], SysParamsModel.deleted == 0).one()
        if param.param_key != vo['param_key']:
            res = db.session.query(SysParamsModel).filter(SysParamsModel.param_key == vo['param_key'], SysParamsModel.deleted == 0).one_or_none()
            if res:
                raise Exception("参数键已存在")
            # 删除之前的缓存信息
            redis.hdel(RedisKeys.get_param_key(), param.param_key)

        # 修改数据
        for key, value in vo.items():
            setattr(param, key, value)
        db.session.commit()

        # 保存到缓存
        redis.hset(RedisKeys.get_param_key(), param.param_key, param.param_value)

    def delete(self, id_list):
        model_list = super().remove_by_ids(id_list)
        for model in model_list:
            redis.hdel(RedisKeys.get_param_key(), model.param_key)
    
    def get_param_key(self, param_key):
        value = redis.hget(RedisKeys.get_param_key(), param_key)
        if not value is None:
            return str(value.decode('utf-8'))
        # 如果缓存没有，则查询数据库
        res = db.session.query(SysParamsModel).filter(SysParamsModel.param_key == param_key, SysParamsModel.deleted == 0).one_or_none()
        if not res:
            raise Exception("参数值不存在，paramKey：" + param_key)
        # 保存到缓存
        redis.hset(RedisKeys.get_param_key(), res.param_key, res.param_value)
        return res.param_value