from db import db
from model import SysUserModel
from . import scheduler

class TimeSchedule:

    @classmethod
    def run(cls):
        with scheduler.app.app_context():
            # 在此处写逻辑
            user_count = db.session.query(SysUserModel).filter(SysUserModel.deleted == 0).count()
            print(f"用户数量{str(user_count)}")
            print("定时任务执行了.......................")

            