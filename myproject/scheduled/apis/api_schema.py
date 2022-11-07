from ninja import Schema
from enum import Enum
from typing import  List,Any


class RemoveJobIn(Schema):
    id:str

class PauseJobIn(Schema):
    id:str

class ResumeJobIn(Schema):
    id:str

class JobSchema(Schema):
    id:str
    next_run_time: Any
    # job_state:Any

class JobListOut(Schema):
    id:Any
    describe: str
    crontab:str
    trigger:str
    excutefun:str
    state:Any
    job:JobSchema=None


class triggerType(str, Enum):
    """请求方法"""
    cron = "cron"

class CreateJonIn(Schema):
    describe: str
    excutefun:str
    trigger:triggerType
    crontab:str="* * * * *"   #分 时 日 月 周

class UpdateJobIn(Schema):
    id:str
    excutefun:str
    crontab: str = "* * * * *"  # 分 时 日 月 周