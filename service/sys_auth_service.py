import uuid
import json
from datetime import datetime, timedelta

from db import redis
from model import SysUserTokenModel
from service import SysCaptchaService, SysUserService, SysMenuService, SysLogLoginService, SysUserTokenService
from common import RedisKeys, Result
from enums import SysLoginStatusEnum, SysLoginOperationEnum
from config import CONFIG


class SysAuthService():

    def login_by_account(self, body):
        # 1.获取参数
        username = body['username']
        password = body['password']
        key = body['key']
        captcha = body['captcha']
        # 3.校验验证码
        if not SysCaptchaService().validate(key, captcha):
            # 保存日志
            SysLogLoginService().save(username=username, status=SysLoginStatusEnum.FAIL.value, operation=SysLoginOperationEnum.CAPTCHA_FAIL.value)        
            raise Exception("验证码错误")
        # 4.用户认证,验证账号和密码和数据库是否匹配
        user = SysUserService().login(username, password)
        # 5.查询User的权限列表
        user.authority_set = SysMenuService().get_user_authority(Result.handle(user))
        # 6.查询这个人的数据范围
        user.data_scope_list = SysUserService().get_data_scope(user)
        # 6.生成accessToken
        access_token = str(uuid.uuid4())
        # 7.保存用户信息到缓存
        redis.set(RedisKeys.get_access_token_key(access_token), json.dumps(Result.handle(user)), CONFIG["APP"]["TOKEN_EXPIRE"])
        create_time = datetime.now()
        access_token_expire = create_time + timedelta(seconds=CONFIG["APP"]["TOKEN_EXPIRE"])
        # 8.保存在线用户到数据库，方便管理在线用户
        SysUserTokenService().save(SysUserTokenModel(user_id=user.id, access_token=access_token, access_token_expire=access_token_expire, create_time=create_time))

        SysLogLoginService().save(username=user.username, status=SysLoginStatusEnum.SUCCESS.value, operation=SysLoginOperationEnum.LOGIN_SUCCESS.value)        
        return { 
            "access_token": access_token
        }
