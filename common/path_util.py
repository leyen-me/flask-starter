class PathUtil:

    @classmethod
    def is_path_allowed(cls, path, white_list):
        for pattern in white_list:
            if "**" in pattern:
                # 去除 "**" 及其之后的部分，只保留前缀进行匹配
                prefix = pattern.split('**')[0]
                if path.startswith(prefix):
                    return True
            elif path == pattern:
                return True
        return False
