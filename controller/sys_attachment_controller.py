from flask import Blueprint as Controller, request

from common import Result
from service import SysAttachmentService
from decorator import has_authority, operate_log

sys_attachment_controller = Controller("sys_attachment", __name__, url_prefix='/sys/attachment')


@sys_attachment_controller.route("/page", methods=['GET'])
@has_authority("sys:attachment:page")
def page():
    return Result.ok(SysAttachmentService().page())


@sys_attachment_controller.route("/", methods=['POST'])
@has_authority("sys:attachment:save")
def save():
    data = request.json
    return Result.ok(SysAttachmentService().save(data))


@sys_attachment_controller.route("/", methods=['DELETE'])
@has_authority("sys:attachment:delete")
def delete():
    data = request.json
    return Result.ok(SysAttachmentService().delete(data))
