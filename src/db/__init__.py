from flask_sqlalchemy import SQLAlchemy
import redis as r

from config import CONFIG

# =========================================关系型数据库==========================================
db = SQLAlchemy()
db_config = {
    "SQLALCHEMY_DATABASE_URI": CONFIG["SQLALCHEMY"]["DATABASE_URI"],
    "SQLALCHEMY_ECHO": CONFIG["SQLALCHEMY"]["SQLALCHEMY_ECHO"]
}
db_table_args = {'mysql_charset': 'utf8mb4', 'mysql_engine': 'InnoDB'}
# =========================================关系型数据库==========================================


# =========================================缓存数据库==========================================
redis_pool = r.ConnectionPool(host=CONFIG["REDIS"]["HOST"], port=CONFIG["REDIS"]["PORT"], db=CONFIG["REDIS"]["DB"],
                              password=CONFIG.get('REDIS', {}).get('PASSWORD'))
redis = r.Redis(connection_pool=redis_pool)
# =========================================缓存数据库===========================================
