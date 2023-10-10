CONFIG = {
    "APP": {
        "PORT": 8080,
        "STATIC_FOLDER": "static",
        "TOKEN_NAME": "Authorization",
        "TOKEN_EXPIRE": 86400,
        "AUTH_WHITE_LIST":[
            "/favicon.ico",
            "/static",
            "/sys/auth/login",
            "/sys/auth/captcha",
            "/sys/auth/captcha/enabled"
        ]
    },
    "REDIS": {
        "HOST": "localhost",
        "PORT": 6379,
        "DB": 0
    },
    "SQLALCHEMY": {
        "DATABASE_URI": f"mysql+pymysql://root:123456@localhost:3306/demo?charset=utf8",
        "POOL_SIZE": 10,
        "POOL_TIMEOUT": 30,
        "POOL_RECYCLE": 3600,
        "TRACK_MODIFICATIONS": False,
        "COMMIT_ON_TEARDOWN": False,
        "SQLALCHEMY_ECHO": True,
    }
}