from flask import Blueprint as Controller, request, g

from common import Result
from service import SysUserService, SysUserRoleService, SysUserPostService
from decorator import has_authority, operate_log
from enums import SysOperateTypeEnum

sys_user_controller = Controller("user", __name__, url_prefix='/sys/user')


@sys_user_controller.route("/page", methods=["GET"])
@has_authority("sys:user:page")
@operate_log(SysOperateTypeEnum.GET)
def page():
    return Result.ok(SysUserService().page())


@sys_user_controller.route("/<int:id>", methods=["GET"])
@has_authority("sys:user:info")
def get(id):
    res = SysUserService().get_by_id(id)
    res.password = ""
    if res:
        res.role_id_list = SysUserRoleService().get_role_id_list(id)
        res.post_id_list = SysUserPostService().get_post_id_list(id)
    return Result.ok(res)


@sys_user_controller.route("/info", methods=["GET"])
def info():
    user = g.user
    return Result.ok(user)


@sys_user_controller.route("/password", methods=["PUT"])
def password():
    data = request.json
    return Result.ok(SysUserService().update_password(data))


@sys_user_controller.route("", methods=["POST"])
@has_authority("sys:user:save")
def save():
    data = request.json
    return Result.ok(SysUserService().save(data))


@sys_user_controller.route("", methods=["PUT"])
@has_authority("sys:user:update")
def update():
    data = request.json
    return Result.ok(SysUserService().update(data))


@sys_user_controller.route("", methods=["DELETE"])
@has_authority("sys:user:delete")
def delete():
    id_list = request.json
    curr_user_id = g.user["id"]
    return Result.ok(SysUserService().delete(curr_user_id, id_list))


@sys_user_controller.route("/import", methods=["POST"])
@has_authority("sys:user:import")
def import_excel():
    trans_dic = {
        "gender": "user_gender",
        "super_admin": "user_super_admin",
        "status": "user_status"
    }
    SysUserService().import_by_excel(trans_dic)
    return Result.ok()


@sys_user_controller.route("/export", methods=["GET"])
@has_authority("sys:user:export")
def export():
    trans_dic = {
        "gender": "user_gender",
        "super_admin": "user_super_admin",
        "status": "user_status"
    }
    return SysUserService().export(trans_dic=trans_dic)
