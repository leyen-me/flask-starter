import uuid
from flask import Blueprint as Controller, request, g
from common import Result
from service import SysPostService
from decorator import has_authority, operate_log
import os
from config import CONFIG

sys_post_controller = Controller("sys_post", __name__, url_prefix='/sys/post')


@sys_post_controller.route("/page")
@has_authority("sys:post:page")
def page():
    return Result.ok(SysPostService().page())


@sys_post_controller.route("/list")
@has_authority("sys:post:page")
def get_list():
    return Result.ok(SysPostService().get_list())


@sys_post_controller.route("/", methods=['POST'])
@has_authority("sys:post:save")
def save():
    body = request.json
    return Result.ok(SysPostService().save(body))


@sys_post_controller.route("/<int:id>", methods=['GET'])
@has_authority("sys:post:info")
def info(id):
    return Result.ok(SysPostService().info(id))


@sys_post_controller.route("/", methods=['PUT'])
@has_authority("sys:post:update")
def update():
    body = request.json
    return Result.ok(SysPostService().update(body))


@sys_post_controller.route("/", methods=["DELETE"])
@has_authority("sys:post:delete")
def delete():
    # 批量删除，得删除列表
    id_list = request.json
    return Result.ok(SysPostService().delete(id_list))
