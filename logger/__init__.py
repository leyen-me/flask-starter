import os
import logging
from datetime import datetime
from logging.handlers import TimedRotatingFileHandler

from config import CONFIG

# 设置日志器的名字
LOGGER_NAME = "FlaskStarterLogger"


def setup_logger():
    """
    开启日志记录，日志会影响接口的效率，请谨慎使用
    """

    sqlalchemy_logger = logging.getLogger('sqlalchemy.engine')
    app_logger = logging.getLogger(LOGGER_NAME)

    if CONFIG['ENV'] == "development":
        app_logger.setLevel(logging.DEBUG)
    elif CONFIG['ENV'] == "production":
        app_logger.setLevel(logging.INFO)
    else:
        app_logger.setLevel(logging.INFO)

    log_levels = ['INFO', 'WARNING', 'ERROR', 'DEBUG', ]
    log_folder = '.logs'

    # 确保日志文件夹和子文件夹存在
    if not os.path.exists(log_folder):
        os.makedirs(log_folder)

    for level in log_levels:
        level_folder = os.path.join(log_folder, level)
        if not os.path.exists(level_folder):
            os.makedirs(level_folder)
        # 按天轮转日志
        handler = TimedRotatingFileHandler(
            os.path.join(level_folder, datetime.now().strftime('%Y-%m-%d') + '.log'),
            when="midnight",
            interval=1,
            backupCount=7,
            encoding='utf-8'
        )
        handler.setLevel(getattr(logging, level))
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        app_logger.addHandler(handler)
        sqlalchemy_logger.addHandler(handler)

    return app_logger


# 初始化并导出日志器
logger = setup_logger()
