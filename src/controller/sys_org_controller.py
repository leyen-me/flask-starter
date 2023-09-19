from flask import Blueprint as Controller, request
from service import SysOrgService
from common import Result
from decorator import has_authority, operate_log
from enums import SysOperateTypeEnum

sys_org_controller = Controller("sys_org", __name__, url_prefix='/sys/org')

@sys_org_controller.route("/list")
@has_authority("sys:org:list")
def list():
    return Result.ok(SysOrgService().get_list())

@sys_org_controller.route("/<int:id>")
@has_authority("sys:org:info")
def info(id):
    return Result.ok(SysOrgService().info(id))

@sys_org_controller.route("/", methods=['POST'])
@has_authority("sys:org:save")
def save():
    body = request.json
    return Result.ok(SysOrgService().save(body))

@sys_org_controller.route("/", methods=['PUT'])
@has_authority("sys:org:update")
def update():
    body = request.json
    return Result.ok(SysOrgService().update(body))

@sys_org_controller.route("/<int:id>", methods=['DELETE'])
@has_authority("sys:org:delete")
def delete(id):
    return Result.ok(SysOrgService().delete(id))