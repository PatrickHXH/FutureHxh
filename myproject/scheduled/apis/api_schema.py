from ninja import Schema
from enum import Enum
from typing import  List,Any


class RemoveJobIn(Schema):
    id:str

class PauseJobIn(Schema):
    id:str

class ResumeJobIn(Schema):
    id:str

class JobListOut(Schema):
    id:Any
    next_run_time:Any
    # job_state:Any

class triggerType(str, Enum):
    """请求方法"""
    cron = "cron"

class CreateJonIn(Schema):
    excutefun:str
    trigger:triggerType
    crontab:str="* * * * *"   #分 时 日 月 周
