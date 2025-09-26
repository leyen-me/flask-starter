from flask import Blueprint as Controller, request

from common import Result
from service import SysDictTypeService
from decorator import has_authority, operate_log

sys_dict_type_controller = Controller("sys_dict_type", __name__, url_prefix='/sys/dict/type')


@sys_dict_type_controller.route("/page", methods=['GET'])
@has_authority("sys:dict:page")
def page():
    return Result.ok(SysDictTypeService().page())


@sys_dict_type_controller.route("/sql/list", methods=['GET'])
@has_authority("sys:dict:page")
def list_sql():
    id = request.args.get('id')
    return Result.ok(SysDictTypeService().get_dict_sql(id))


@sys_dict_type_controller.route("/<int:id>", methods=['GET'])
@has_authority("sys:dict:info")
def info(id):
    return Result.ok(SysDictTypeService().info(id))


@sys_dict_type_controller.route("", methods=['POST'])
@has_authority("sys:dict:save")
def save():
    data = request.json
    return Result.ok(SysDictTypeService().save(data))


@sys_dict_type_controller.route("", methods=['PUT'])
@has_authority("sys:dict:update")
def update():
    data = request.json
    return Result.ok(SysDictTypeService().update(data))


@sys_dict_type_controller.route("", methods=['DELETE'])
@has_authority("sys:dict:delete")
def delete():
    data = request.json
    return Result.ok(SysDictTypeService().delete(data))


@sys_dict_type_controller.route("/all")
def all():
    return Result.ok(SysDictTypeService().get_dict_list())
