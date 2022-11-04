from ninja import Router
from django.shortcuts import render
from reports.apis.ReportsCommon import SearchReport
from myproject.settings import BASE_DIR
from reports.models import ProjectManage
from myproject.common import response, Error
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from scheduled.jobs.SearchReportJob import Search_Report
from scheduled.apis.api_schema import RemoveJobIn,PauseJobIn,JobListOut,ResumeJobIn,CreateJonIn
from django_apscheduler.models import DjangoJob, DjangoJobExecution
from myproject.pagination import CustomPagination
from ninja.pagination import paginate,PageNumberPagination  #分页
from typing import  List,Any
import os
import datetime

router = Router(tags=["scheduled"])

scheduler = BackgroundScheduler(timezone='Asia/Shanghai')
scheduler.add_jobstore(DjangoJobStore(), 'default')


#创建定时任务
@router.post("/create/")
def createjob(request,data:CreateJonIn):
        #执行函数
        excutefun = data.excutefun
        #触发类型
        trigger = data.trigger
        #触发时间
        crontab = data.crontab
        try:
                scheduler.add_job(globals()[excutefun], CronTrigger.from_crontab(crontab))
                register_events(scheduler)
                scheduler.start()
                return response()
        except:
                return response()

#移除定时任务
@router.post("/removejob/")
def removejob(request,data:RemoveJobIn):
        try:
                scheduler.start()
                scheduler.remove_job(data.id)
                return response()
        except:
                scheduler.remove_job(data.id)
                return response()

#暂停定时任务
@router.post("/pausejob/")
def pausejob(request,data:PauseJobIn):
        try:
                scheduler.start()
                scheduler.pause_job(data.id)
                return response()
        except:
                scheduler.pause_job(data.id)
                return response()

#重启定时任务
@router.post("/resumejob/")
def resumejob(request,data:ResumeJobIn):
        try:
                scheduler.start()
                scheduler.resume_job(data.id)
                return response()
        except:
                scheduler.resume_job(data.id)
                return response()

#获取任务
@router.get("/joblist/",response=List[JobListOut])
@paginate(CustomPagination)
def getjobs(request):
        obj = DjangoJob.objects.all()
        return obj

