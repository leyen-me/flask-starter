from flask import Blueprint as Controller, request

from service import SysCaptchaService, SysAuthService
from common import Result

sys_auth_controller = Controller("sys_auth", __name__, url_prefix='/sys/auth')


@sys_auth_controller.route("/captcha", methods=["GET"])
def captcha():
    return Result.ok(SysCaptchaService().generate())


@sys_auth_controller.route("/captcha/enabled", methods=["GET"])
def captcha_enabled():
    return Result.ok(SysCaptchaService().is_captcha_enabled())


@sys_auth_controller.route("/login", methods=["POST"])
def login():
    data = request.json
    return Result.ok(SysAuthService().login_by_account(data))


@sys_auth_controller.route("/logout", methods=["POST"])
def logout():
    # todo：退出登录逻辑
    return Result.ok("退出成功")
