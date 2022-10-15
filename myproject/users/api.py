from ninja import Router
from myproject.common import response, Error, TokenMethod
from django.contrib.auth.models import User
from django.contrib import auth
from users.api_schema import RegisterIn, LoginIn,TokenIn,TokenOut
import pickle
import base64
import json
import time
from django.core import signing
import hashlib
from django.core.cache import cache

router = Router(tags=["users"])

# 注册
@router.post("/register",auth=None)
def user_register(request,payload:RegisterIn):
    if payload.password != payload.confirm_password:
        return response(error=Error.PAWD_ERROR)
    try:
        User.objects.get(username=payload.username)
    except User.DoesNotExist:
        pass
    else:
        return response(error=Error.USER_EXIST)
    user = User.objects.create_user(username=payload.username,password=payload.password)
    user_info = {
        "id": user.id,
        "username":user.username
    }
    return response(result=user_info)

#登陆
@router.post("/login",auth=None)
def testtoken(request,data:LoginIn):
    """
    假设，必须要登录之后才能访问
    测试：获取toekn
    """
    username = data.username
    password  = data.password
    if username == "" or password =="":
        return  response(error=Error.USER_OR_PAWD_NULL)
    else:
        user = auth.authenticate(username=username,password=password)
        if user is not None:
            print(type(user.username))
            token = TokenMethod.create_token(user.username)
            user_info = {
                "id": user.id,
                "username": user.username,
                "token": token
            }
            return response(result = user_info)
        else:
            return response(error=Error.USER_OR_PAWD_EROOR)

#获取用户信息
@router.post("/getinfo/")
def get_info(request,data:TokenIn):
    token = data.token
    lasttoken = TokenMethod.check_token(token)
    username = TokenMethod.get_username(token)
    info = {
        "username":username,
        "checkout":lasttoken
    }
    return response(result=info)

#登出
@router.post("/logout/")
def delete_token(request,data:TokenOut):
    '''
    退出登陆
    '''
    TokenMethod.delete_token(data.username)
    return  response()