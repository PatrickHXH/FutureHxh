from ninja import Schema
from enum import Enum
from typing import  List,Any

class SourceType(str,Enum):
    VCDUI = "V车店UI"
    VCDAPI = "V车店API"
    VQDAPI = "V渠道API"
    CXGJUI = "车险管家UI"

class SearchReport(Schema):
    """获取报告列表入参"""
    source:SourceType
    reportime:str
    email_user:str
    password:str
    server:str


class ReaportLogIn(Schema):
    source:SourceType
    reportime:str

class ReaportLogOut(Schema):
    id:int
    sender:str
    receive:str
    # text:Any
    source:SourceType
    report_time:Any
    create_time: Any
    update_time: Any

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