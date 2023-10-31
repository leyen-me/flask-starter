class RedisKeys:

    @classmethod
    def get_captcha_key(cls, key):
        return "sys:captcha:" + key

    @classmethod
    def get_access_token_key(cls, access_token):
        return "sys:token:" + access_token

    @classmethod
    def get_param_key(cls):
        return "system:params"
    
    @classmethod
    def get_dict_key(cls):
        return "system:dict"

