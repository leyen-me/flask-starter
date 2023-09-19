class RedisKeys:
    def getCaptchaKey(key):
        return "sys:captcha:" + key

    def getAccessTokenKey(access_token):
        return "sys:token:" + access_token

    def getParamKey():
        return "system:params"
