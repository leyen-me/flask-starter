from flask import Blueprint as Controller, request

from common import Result
from service import SysDictDataService
from decorator import has_authority, operate_log

sys_dict_data_controller = Controller("sys_dict_data", __name__, url_prefix='/sys/dict/data')


@sys_dict_data_controller.route("/page", methods=['GET'])
@has_authority("sys:dict:page")
def page():
    dict_type_id = request.args.get("dict_type_id")
    return Result.ok(SysDictDataService().page(dict_type_id))


@sys_dict_data_controller.route("/<int:id>", methods=['GET'])
@has_authority("sys:dict:info")
def info(id):
    return Result.ok(SysDictDataService().info(id))


@sys_dict_data_controller.route("", methods=['POST'])
@has_authority("sys:dict:save")
def save():
    data = request.json
    return Result.ok(SysDictDataService().save(data))


@sys_dict_data_controller.route("", methods=['PUT'])
@has_authority("sys:dict:update")
def update():
    data = request.json
    return Result.ok(SysDictDataService().update(data))


@sys_dict_data_controller.route("", methods=['DELETE'])
@has_authority("sys:dict:delete")
def delete():
    data = request.json
    return Result.ok(SysDictDataService().delete(data))
