from ninja import Router
from ninja import Schema
from django.shortcuts import render
from myproject.common import response, Error
import datetime

router = Router(tags=["performance"])

@router.post("/account/create/")
#保存远程服务账号
def account_create(request):
    '''
    保存远程服务账号
    '''

    return response()