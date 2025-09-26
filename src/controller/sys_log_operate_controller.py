from flask import Blueprint as Controller

from service import SysLogOperateService
from common import Result
from decorator import has_authority, operate_log

sys_log_operate_controller = Controller("sys_log_operate", __name__, url_prefix='/sys/log/operate')


@sys_log_operate_controller.route("/page", methods=['GET'])
@has_authority("sys:operate:all")
def page():
    return Result.ok(SysLogOperateService().page())
