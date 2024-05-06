from flask import Blueprint as Controller, request

from common import Result
from service import SysFileUploadService

sys_file_upload_controller = Controller("sys_file_upload", __name__, url_prefix='/sys/file/upload')


@sys_file_upload_controller.route("", methods=['POST'])
def upload():
    data = request.files
    return Result.ok(SysFileUploadService().upload(data))
