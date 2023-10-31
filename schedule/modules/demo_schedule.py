from db import db
from model import SysUserModel
from schedule import scheduler


class DemoSchedule:

    @classmethod
    def run(cls):
        with scheduler.app.app_context():
            # 在此处写逻辑
            print("定时任务开始========================>")
            user_count = db.session.query(SysUserModel).filter(SysUserModel.deleted == 0).count()
            print(f"一共有{str(user_count)}个用户")
            print("定时任务结束========================>")
