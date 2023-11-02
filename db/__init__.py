from flask_sqlalchemy import SQLAlchemy
import redis as r

from config import CONFIG

# =========================================关系型数据库==========================================
db = SQLAlchemy()
# =========================================关系型数据库==========================================


# =========================================缓存数据库==========================================
redis_pool = r.ConnectionPool(host=CONFIG["REDIS"]["HOST"], port=CONFIG["REDIS"]["PORT"], db=CONFIG["REDIS"]["DB"],
                              password=CONFIG.get('REDIS', {}).get('PASSWORD'))
redis = r.Redis(connection_pool=redis_pool)
# =========================================缓存数据库===========================================
