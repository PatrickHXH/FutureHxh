from ninja import Router
from myproject.common import response, Error
from reports.models import EmailManage
from reports.apis.api_schema import EmailIn,EmailOut
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from myproject.pagination import CustomPagination
from ninja.pagination import paginate,PageNumberPagination  #分页
from typing import  List,Any

router = Router(tags=["email"])

# 邮箱管理，增、删、改、查（详情、列表）
#创建邮箱
@router.post("/create/")
def create_email(request,data:EmailIn):
        EmailManage.objects.create(**data.dict())
        return response()

#更新邮箱
@router.post("/update/{id}/")
def update_email(request,id:int,data:EmailIn):
        obj = get_object_or_404(EmailManage,id=id)
        print(data.dict().items())
        for attr,value in data.dict().items():
                setattr(obj,attr,value)
        obj.save()
        obj = EmailManage.objects.get(pk=id)
        return response(result=model_to_dict(obj))

#删除邮件
@router.post("/delete/{id}/")
def delete_email(request,id:int):
        try:
                get_object_or_404(EmailManage, id=id)
                EmailManage.objects.filter(id=id).delete()
        except:
                return response(error=Error.EMAIL_ID_NOT_EXISTS)
        return response()

#获取邮件详情
@router.get("/detail/{id}/")
def get_email(request,id:int):
        obj = get_object_or_404(EmailManage, id=id)
        return response(result=model_to_dict(obj))

#获取邮件列表
@router.get("/list/",response=List[EmailOut])
@paginate(CustomPagination)
def email_list(request):
        obj =EmailManage.objects.filter().all()
        return obj