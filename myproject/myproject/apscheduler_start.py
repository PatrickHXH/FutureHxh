import logging
from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore

logger = logging.getLogger('scheduler_log')
logger.setLevel(logging.DEBUG)

jobstores = {
    'default': DjangoJobStore()
}
job_defaults = {
    'coalesce': True,
    'max_instances': 1,
    'misfire_grace_time': 60,
    'replace_existing': True
}
scheduler = BackgroundScheduler(jobstores=jobstores, job_defaults=job_defaults)
# pool_pre_ping为True，即每次从连接池中取连接的时候，都会验证一下与数据库是否连接正常，如果没有连接，那么该连接会被回收。
# engine_options={'pool_pre_ping': True, 'pool_recycle': 100}
scheduler.start()

def listener_event(event):
    job_id = event.job_id
    scheduled_run_time = event.scheduled_run_time.strftime("%Y-%m-%d %H:%M:%S")
    if event.exception:
        logger.error('作业ID：{} 在 {} 执行失败，错误原因：{}'.format(job_id, scheduled_run_time, event.exception.args[0]))


scheduler._logger = logger
# 当任务执行完或任务出错时，listener_event
scheduler.add_listener(listener_event, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)


# 使用main_loop阻塞进程,防止进程挂起
# import time
# while True:
#     time.sleep(60)
#     sig = uwsgi.signal_wait()