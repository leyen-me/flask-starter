from flask import Blueprint as Controller

from service import SysLogLoginService
from common import Result
from decorator import has_authority, operate_log


sys_log_login_controller = Controller("sys_log_login", __name__, url_prefix='/sys/log/login')

@sys_log_login_controller.route("/page", methods=['GET'])
@has_authority("sys:log:login")
def page():
    return Result.ok(SysLogLoginService().page())

@sys_log_login_controller.route("/export", methods=['GET'])
@has_authority("sys:log:login")
def export():
    return SysLogLoginService().export()

@sys_log_login_controller.route("/", methods=['POST'])
@has_authority("sys:log:login")
def save():
    return Result.ok(SysLogLoginService().save('1',11,2))