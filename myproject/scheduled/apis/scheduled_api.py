from ninja import Router
from django.shortcuts import render
from reports.apis.ReportsCommon import SearchReport
from myproject.settings import BASE_DIR
from reports.models import ProjectManage
from myproject.common import response, Error
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from myproject.apscheduler_start import scheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events, register_job
from scheduled.jobs.SearchReportJob import Search_Report,Search_Report_lastest
from scheduled.apis.api_schema import RemoveJobIn,PauseJobIn,JobListOut,ResumeJobIn,CreateJonIn,JobSchema,UpdateJobIn
from django_apscheduler.models import DjangoJob, DjangoJobExecution
from scheduled.models import DjangoJobExtend
from myproject.pagination import CustomPagination
from ninja.pagination import paginate,PageNumberPagination  #分页
from django.forms.models import model_to_dict
from django.shortcuts import get_object_or_404
import base64
from typing import  List,Any
import os
import datetime

router = Router(tags=["scheduled"])

#创建定时任务
@router.post("/create/")
def createjob(request,data:CreateJonIn):
        #执行函数
        excutefun = data.excutefun
        #触发类型
        trigger = data.trigger
        #触发时间
        crontab = data.crontab
        #描述
        describe=data.describe
        try:
                obj = scheduler.add_job(globals()[excutefun], CronTrigger.from_crontab(crontab))
        except Exception as e:
                logger.error(e)
        DjangoJobExtend.objects.create(job_id=obj.id,describe=describe,trigger=trigger,excutefun=excutefun,crontab=crontab)
        return response(result=obj.id)


#移除定时任务
@router.post("/removejob/")
def removejob(request,data:RemoveJobIn):
        scheduler.remove_job(data.id)
        return response()


#暂停定时任务
@router.post("/pausejob/")
def pausejob(request,data:PauseJobIn):
        # try:
        # scheduler.start()
        scheduler.pause_job(data.id)
        obj = DjangoJob.objects.get(id=data.id)
        if obj.next_run_time is None:
                obj_extend = DjangoJobExtend.objects.get(job_id=data.id)
                obj_extend.state = 0
                obj_extend.save()
        return response()

#重启定时任务
@router.post("/resumejob/")
def resumejob(request,data:ResumeJobIn):
        # try:
        # scheduler.start()
        scheduler.resume_job(data.id)
        obj = DjangoJob.objects.get(id=data.id)
        if obj.next_run_time is not None:
                obj_extend = DjangoJobExtend.objects.get(job_id=data.id)
                obj_extend.state = 1
                obj_extend.save()
        return response()

#获取任务列表
@router.get("/joblist/",response=List[JobListOut])
@paginate(CustomPagination)
def getjobs(request):
        obj = DjangoJobExtend.objects.all()
        return obj

#获取任务详情
@router.get("/jobdetail/{id}/")
def getjobdetail(request,id:int):
        obj = DjangoJobExtend.objects.get(id=id)
        obj_job = DjangoJob.objects.get(id=obj.job_id)
        obj_job_dict = model_to_dict(obj_job)
        obj_dict = model_to_dict(obj)
        obj_dict["job"] = obj_job_dict
        obj_dict["job"]["next_run_time"] =obj_dict["job"]["next_run_time"].strftime("%Y-%m-%d %H:%M:%S")
        return response(result=obj_dict)


