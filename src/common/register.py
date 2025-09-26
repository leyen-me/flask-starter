import json

from flask_cors import CORS
from flask import Flask, request, g

from logger import logger
from config import CONFIG
from db import db, redis, db_config
from db.initialize import Initialize
from schedule import scheduler
from schedule.modules.demo_schedule import DemoSchedule
from schedule.modules.dict_schedule import DictSchedule
from apscheduler.triggers.cron import CronTrigger
from common import RedisKeys, Result, PathUtil
from enums import SysUserStatusEnum
from controller import *

class Register:

    # 开启关系型数据库
    @classmethod
    def register_db(cls, app: Flask):
        app.config.update(db_config)
        db.init_app(app)

    # 关系型数据库数据初始化
    # 创建表，和初始化数据
    @classmethod
    def register_db_data_init(cls, app: Flask):
        with app.app_context():
            Initialize.init()

    # 开启跨域访问
    @classmethod
    def register_cors(cls, app: Flask):
        CORS(app, supports_credentials=True, resources=r"/*")

    # 开启任务
    @classmethod
    def register_scheduler(cls, app: Flask):
        scheduler.init_app(app)
        scheduler.add_job(id='time_schedule', func=DemoSchedule.run, trigger=CronTrigger.from_crontab("28 10 * * *"))

        # 字典缓存，主要用于导入、导出时候的翻译
        DictSchedule.run()
        scheduler.add_job(id='dict_schedule', func=DictSchedule.run, trigger=CronTrigger.from_crontab("00 00 * * *"))

        scheduler.start()

    # 开启接口鉴权
    @classmethod
    def register_auth(cls, app: Flask):
        @app.before_request
        def before():
            # 跳过OPTIONS请求
            if request.method == 'OPTIONS':
                return
            # 检查白名单
            if PathUtil.is_path_allowed(request.path, CONFIG["APP"]["AUTH_WHITE_LIST"]):
                return
            # 检查TOKEN_NAME
            access_token = request.headers.get(CONFIG["APP"]["TOKEN_NAME"])
            if access_token is None:
                raise Exception("用户未登录")
            # 去REDIS检查用户信息
            user_str = redis.get(RedisKeys.get_access_token_key(access_token))
            if user_str:
                g.user = json.loads(user_str)
                if g.user['status'] == SysUserStatusEnum.DISABLE.value:
                    raise Exception("账号已被停用")
            else:
                raise Exception("登录已过期")

    # 开启异常拦截
    @classmethod
    def register_exception(cls, app: Flask):
        @app.errorhandler(Exception)
        def exception(error_msg):
            logger.error(f'{request.path} - {request.method} - {error_msg}')
            return Result.error(str(error_msg))

    # 注册路由
    @classmethod
    def register_controller(cls, app: Flask):
        app.register_blueprint(sys_auth_controller)
        app.register_blueprint(sys_user_controller)
        app.register_blueprint(sys_menu_controller)
        app.register_blueprint(sys_dict_type_controller)
        app.register_blueprint(sys_dict_data_controller)
        app.register_blueprint(sys_org_controller)
        app.register_blueprint(sys_post_controller)
        app.register_blueprint(sys_role_controller)
        app.register_blueprint(sys_params_controller)
        app.register_blueprint(sys_attachment_controller)
        app.register_blueprint(sys_file_upload_controller)
        app.register_blueprint(sys_log_login_controller)
        app.register_blueprint(sys_log_operate_controller)

    # 注册静态文件路由
    @classmethod
    def register_static_controller(cls, app: Flask):
        app.static_folder = CONFIG["APP"]["STATIC_FOLDER"]
