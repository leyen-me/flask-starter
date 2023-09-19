import json
from datetime import datetime
from flask import Flask, request, g
from flask_cors import CORS
from sqlalchemy import event

from db import db, redis
from model import *
from controller import *
from common import RedisKeys, Result
from config import CONFIG
from schedule import scheduler
from db.initialize import Initialize

app = Flask(__name__, static_folder=CONFIG["APP"]["STATIC_FOLDER"])

# 设置数据库连接地址
app.config["SQLALCHEMY_DATABASE_URI"] = CONFIG["SQLALCHEMY"]["DATABASE_URI"]
# 连接池大小
app.config['SQLALCHEMY_POOL_SIZE'] = CONFIG["SQLALCHEMY"]["POOL_SIZE"]
# 连接池超时时间为30秒，人太多了，供不应求
app.config['SQLALCHEMY_POOL_TIMEOUT'] = CONFIG["SQLALCHEMY"]["POOL_TIMEOUT"]
# 3600秒后重新连接，连接被回收，创建新的连接
app.config['SQLALCHEMY_POOL_RECYCLE'] = CONFIG["SQLALCHEMY"]["POOL_RECYCLE"]
# 是否追踪数据库修改(开启后会触发一些钩子函数)  一般不开启, 会影响性能
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = CONFIG["SQLALCHEMY"]["TRACK_MODIFICATIONS"]
# 控制在请求处理结束时是否自动提交数据库会话
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = CONFIG["SQLALCHEMY"]["COMMIT_ON_TEARDOWN"]
# 显示SQL执行的语句
app.config['SQLALCHEMY_ECHO'] = CONFIG["SQLALCHEMY"]["SQLALCHEMY_ECHO"]
# 处理跨域
CORS(app, supports_credentials=True, resources=r"/*")

# 初始化数据库
db.init_app(app)
with app.app_context():
    # 创建表，和初始化数据
    Initialize.init()
# 初始化任务调度器
scheduler.init_app(app)

@event.listens_for(SysBaseModel, "before_insert", propagate=True)
def before_insert_listener(mapper, connection, model):
    model.creator = g.user["id"] if model.creator is None else model.creator
    model.updater = g.user["id"] if model.updater is None else model.updater

@event.listens_for(SysBaseModel, 'before_update', propagate=True)
def before_update_listener(mapper, connection, model):
    if (str(type(model.version))=="<class 'int'>"):
        model.version = model.version + 1
    model.updater     = g.user["id"]
    model.update_time = datetime.now()

@app.before_request
def before():
    for white_path in CONFIG["APP"]["AUTH_WHITE_LIST"]:
        if white_path in request.path:
            return
    try:
        access_token = request.headers[CONFIG["APP"]["TOKEN_NAME"]]
    except:
        raise Exception("用户未登录")
    
    user_str = redis.get(RedisKeys.getAccessTokenKey(access_token))
    if user_str:
        g.user = json.loads(user_str)
    else:
        raise Exception("登录已过期")

@app.errorhandler(KeyError)
def handle_key_error(error):
    return Result.error("缺少参数->"+str(error))

# @app.errorhandler(Exception)
# def exception(error_msg):
#     return Result.error(error_msg)

@app.after_request
def after_request(response):
    return response


# =========================================注册路由START=========================================#
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
# =========================================注册路由E N D=========================================#


if __name__ == '__main__':
    # 启动调度器
    scheduler.start()
    # 启动App
    app.run(host='0.0.0.0', port=CONFIG["APP"]["PORT"], debug=True)