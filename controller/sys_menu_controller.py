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
    return Result.ok(SysMenuService().get_user_authority(g.user))

@sys_menu_controller.route("/list", methods=['GET'])
@has_authority("sys:menu:list")
def list():
    # 菜单类型 0：菜单 1：按钮  2：接口  null：全部
    mtype   = request.args.get('type')
    return Result.ok(SysMenuService().get_menu_list(mtype))

@sys_menu_controller.route("/<int:id>", methods=['GET'])
@has_authority("sys:menu:info")
def info(id):
    return Result.ok(SysMenuService().info(id))

@sys_menu_controller.route("/", methods=['POST'])
@has_authority("sys:menu:save")
def save():
    return Result.ok(SysMenuService().save(request.json))

@sys_menu_controller.route("/", methods=['PUT'])
@has_authority("sys:menu:update")
def update():
    return Result.ok(SysMenuService().update(request.json))

@sys_menu_controller.route("/<int:id>", methods=['DELETE'])
@has_authority("sys:menu:delete")
def delete(id):
    return Result.ok(SysMenuService().delete(id))