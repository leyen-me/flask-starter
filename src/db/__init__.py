from flask_sqlalchemy import SQLAlchemy
import redis as r

from config import CONFIG



# =========================================数据库START=========================================#
db = SQLAlchemy()
# =========================================数据库E N D=========================================#



# =========================================缓 存 START=========================================#
redis_pool = r.ConnectionPool(host=CONFIG["REDIS"]["HOST"], port=CONFIG["REDIS"]["PORT"], db=CONFIG["REDIS"]["DB"])
redis = r.Redis(connection_pool=redis_pool)
# =========================================缓 存 E N D=========================================#