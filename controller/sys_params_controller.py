from flask import Blueprint as Controller, request
from common import Result
from service import SysParamsService
from decorator import has_authority, operate_log

sys_params_controller = Controller("sys_params", __name__, url_prefix='/sys/params')

@sys_params_controller.route("/page", methods=['GET'])
@has_authority("sys:params:all")
def page():
    return Result.ok(SysParamsService().page())

@sys_params_controller.route("/<int:id>", methods=['GET'])
@has_authority("sys:params:all")
def info(id):
    return Result.ok(SysParamsService().info(id))

@sys_params_controller.route("/", methods=['POST'])
@has_authority("sys:params:all")
def save():
    return Result.ok(SysParamsService().save(request.json))

@sys_params_controller.route("/", methods=['PUT'])
@has_authority("sys:params:all")
def update():
    return Result.ok(SysParamsService().update(request.json))

@sys_params_controller.route("/", methods=['DELETE'])
@has_authority("sys:params:all")
def delete():
    return Result.ok(SysParamsService().delete(request.json))