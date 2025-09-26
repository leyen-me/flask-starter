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
    trans_dic = {
        "operation": "login_operation",
        "status": "success_fail"
    }
    return SysLogLoginService().export(trans_dic=trans_dic)
