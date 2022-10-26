from ninja import Schema
from enum import Enum
from typing import  List,Any


class SearchReportIn(Schema):
    """获取报告列表入参"""
    project_id:int
    email_id:int


class ProjectSchema(Schema):
    id: int
    name: str
    keyword:str

class SearchReportLogOut(Schema):
    """获取报告列表出参"""
    subject:str
    sender:str
    receive:str
    report_time:Any
    report_dir:str
    project:ProjectSchema=None
    lastest:bool
    existfail:bool
    update_time: Any
    create_time: Any


class DownloadReportIn(Schema):
    email_code:int
    email_id:int

class EmailIn(Schema):
    email:str
    code:str
    server:str

class EmailOut(Schema):
    id:int
    email: str
    code: str
    server: str
    create_time: Any
    update_time: Any

class ProjectIn(Schema):
    name:str
    keyword:str

class ProjectOut(Schema):
    id:int
    name:str
    keyword:str
    create_time: Any
    update_time: Any

