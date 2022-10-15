from ninja import Router
from myproject.common import response, Error
from reports.models import ProjectManage
from reports.apis.api_schema import ProjectIn,ProjectOut
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
from myproject.pagination import CustomPagination
from ninja.pagination import paginate,PageNumberPagination  #分页
from typing import  List,Any

router = Router(tags=["project"])

# 项目管理，增、删、改、查（详情、列表）
#创建项目
@router.post("/create/")
def create_project(request,data:ProjectIn):
        ProjectManage.objects.create(**data.dict())
        return response()

#更新项目
@router.post("/update/{id}/")
def update_project(request,id:int,data:ProjectIn):
        obj = get_object_or_404(ProjectManage,id=id)
        print(data.dict().items())
        for attr,value in data.dict().items():
                setattr(obj,attr,value)
        obj.save()
        obj = ProjectManage.objects.get(pk=id)
        return response(result=model_to_dict(obj))

#删除项目
@router.post("/delete/{id}/")
def delete_project(request,id:int):
        try:
                get_object_or_404(ProjectManage, id=id)
                ProjectManage.objects.filter(id=id).delete()
        except:
                return response(error=Error.PROJECT_ID_NOT_EXISTS)
        return response()

#获取项目详情
@router.get("/detail/{id}/")
def get_project(request,id:int):
        obj = get_object_or_404(ProjectManage, id=id)
        return response(result=model_to_dict(obj))

#获取项目列表
@router.get("/list/",response=List[ProjectOut])
@paginate(CustomPagination)
def project_list(request):
        obj =ProjectManage.objects.filter().all()
        return obj