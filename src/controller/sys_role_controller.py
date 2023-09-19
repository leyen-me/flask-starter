from flask import Blueprint as Controller, request, g
from service import SysRoleService, SysRoleMenuService, SysRoleDataScopeService, SysMenuService, SysUserService, SysUserRoleService
from common import Result
from decorator import has_authority, operate_log

sys_role_controller = Controller("sys_role", __name__, url_prefix='/sys/role')


@sys_role_controller.route("/page")
@has_authority("sys:role:page")
def page():
    return Result.ok(SysRoleService().page())

@sys_role_controller.route("/list")
@has_authority("sys:role:list")
def list():
    return Result.ok(SysRoleService().get_list())

@sys_role_controller.route("/<int:id>")
@has_authority("sys:role:info")
def info(id):
    role = SysRoleService().info(id)
    role.menu_id_list = SysRoleMenuService().get_menu_id_list(id)
    role.org_id_list = SysRoleDataScopeService().get_org_id_list(id)
    return Result.ok(role)

@sys_role_controller.route("/", methods=['POST'])
@has_authority("sys:role:save")
def save():
    body = request.json
    return Result.ok(SysRoleService().save(body))

@sys_role_controller.route("/", methods=['PUT'])
@has_authority("sys:role:update")
def update():
    body = request.json
    return Result.ok(SysRoleService().update(body))

@sys_role_controller.route("/data-scope", methods=['PUT'])
@has_authority("sys:role:update")
def data_scope():
    return Result.ok(SysRoleService().data_scope(request.json))

@sys_role_controller.route("/", methods=['DELETE'])
@has_authority("sys:role:delete")
def delete():
    return Result.ok(SysRoleService().delete(request.json))

@sys_role_controller.route("/menu", methods=['GET'])
@has_authority("sys:role:menu")
def menu():
    return Result.ok(SysMenuService().get_user_menu_list(g.user, None))

@sys_role_controller.route("/user/page", methods=['GET'])
@has_authority("sys:role:update")
def user_page():
    return Result.ok(SysUserService().role_user_page())

@sys_role_controller.route("/user/<int:roleId>", methods=['DELETE'])
@has_authority("sys:role:update")
def user_delete(roleId):
    return Result.ok(SysUserRoleService().delete_by_role_id_user_id_list(roleId, request.json))

@sys_role_controller.route("/user/<int:roleId>", methods=['POST'])
@has_authority("sys:role:update")
def user_save(roleId):
    return Result.ok(SysUserRoleService().save_user_list(roleId, request.json))