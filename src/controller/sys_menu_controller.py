from flask import Blueprint as Controller, request, g

from service import SysMenuService
from common import Result
from decorator import has_authority, operate_log

sys_menu_controller = Controller("sys_menu", __name__, url_prefix='/sys/menu')


@sys_menu_controller.route("/nav", methods=['GET'])
def nav():
    return Result.ok(SysMenuService().get_user_menu_tree(g.user, 0))


@sys_menu_controller.route("/authority", methods=['GET'])
def authority():
    user = g.user
    return Result.ok(SysMenuService().get_user_authority(user))


@sys_menu_controller.route("/list", methods=['GET'])
@has_authority("sys:menu:list")
def list():
    _type = request.args.get('type')
    return Result.ok(SysMenuService().get_menu_list(_type))


@sys_menu_controller.route("/<int:id>", methods=['GET'])
@has_authority("sys:menu:info")
def info(id):
    return Result.ok(SysMenuService().info(id))


@sys_menu_controller.route("", methods=['POST'])
@has_authority("sys:menu:save")
def save():
    data = request.json
    return Result.ok(SysMenuService().save(data))


@sys_menu_controller.route("", methods=['PUT'])
@has_authority("sys:menu:update")
def update():
    data = request.json
    return Result.ok(SysMenuService().update(data))


@sys_menu_controller.route("/<int:id>", methods=['DELETE'])
@has_authority("sys:menu:delete")
def delete(id):
    return Result.ok(SysMenuService().delete(id))
