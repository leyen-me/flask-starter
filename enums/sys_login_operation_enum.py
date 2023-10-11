from enum import Enum



class SysLoginOperationEnum(Enum):
    # 登录成功
    LOGIN_SUCCESS = 0
    # 退出成功
    LOGOUT_SUCCESS = 1
    # 验证码错误
    CAPTCHA_FAIL = 2
    # 账号密码错误
    ACCOUNT_FAIL = 3