import os

# 生产环境，自动切换为 production_config
if 'gunicorn' in os.environ.get('SERVER_SOFTWARE', ''):
    from .production_config import CONFIG as _CONFIG
else:
    from .development_config import CONFIG as _CONFIG

CONFIG = _CONFIG
