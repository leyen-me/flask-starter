from flask_apscheduler import APScheduler
from apscheduler.triggers.cron import CronTrigger

# 定时任务调度器
scheduler = APScheduler()

# 添加定时任务
from .time_schedule import TimeSchedule as TimeSchedule
scheduler.add_job(id='time_schedule',func=TimeSchedule.run, trigger=CronTrigger.from_crontab("21 10 * * *"))