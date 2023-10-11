import uuid
from flask import Blueprint as Controller,request, g
from common import Result
from service import SysUserService,SysUserRoleService,SysUserPostService
from decorator import has_authority, operate_log
import os
from config import CONFIG

sys_user_controller = Controller("user", __name__, url_prefix='/sys/user')

@sys_user_controller.route("/page")
@has_authority("sys:user:page")
def page():
    return Result.ok(SysUserService().page())

@sys_user_controller.route("/<int:id>")
@has_authority("sys:user:info")
def get(id):
    res = SysUserService().get_by_id(id)
    res.password = ""
    if res:
        res.role_id_list = SysUserRoleService().get_role_id_list(id)
        res.post_id_list = SysUserPostService().get_post_id_list(id)
    return Result.ok(res)

@sys_user_controller.route("/info")
def info(): 
    return Result.ok(g.user)

@sys_user_controller.route("/password", methods=["PUT"])
def password():
    body = request.json
    return Result.ok(SysUserService().update_password(body))

@sys_user_controller.route("/", methods=["POST"])
@has_authority("sys:user:save")
def save():
    body = request.json
    return Result.ok(SysUserService().save(body))

@sys_user_controller.route("/", methods=["PUT"])
@has_authority("sys:user:update")
def update():
    body = request.json
    return Result.ok(SysUserService().update(body))

@sys_user_controller.route("/",methods=["DELETE"])
@has_authority("sys:user:delete")
def delete():
    # 批量删除，得删除列表
    id_list = request.json
    curr_user_id = g.user["id"]
    return Result.ok(SysUserService().delete(curr_user_id, id_list))

@sys_user_controller.route("/import", methods=["POST"])
@has_authority("sys:user:import")
def importExcel():
    if 'file' in request.files:
        file = request.files['file']
        file_name = str(uuid.uuid4()) + os.path.splitext(file.filename)[-1]
        file_folder = os.path.join(CONFIG['APP']['STATIC_FOLDER'])
        file_path = os.path.join(os.getcwd(), file_folder, file_name)
        file.save(file_path)
        SysUserService().import_by_excel(file_path)
    return Result.ok()

@sys_user_controller.route("/export", methods=["GET"])
@has_authority("sys:user:export")
def export():
    return SysUserService().export()