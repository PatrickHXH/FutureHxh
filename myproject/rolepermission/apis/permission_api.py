from ninja import Router
from myproject.common import response, Error, TokenMethod
from django.contrib.auth.models import User
from django.contrib import auth
from rolepermission.models import permission_api
from django.contrib.auth.models import Group,User,Permission
from rolepermission.apis.api_schema import  PermissionIn,RolePermissionIn,DeletePermissionIn,DetailPermissionIn,RolePermissionOut,PermissionSchema,APISchemaOut,APISchemaIn,UpdatePermissionIn,addRoleIn
from typing import  List,Any
from myproject.pagination import CustomPagination #自定义分页
from ninja.pagination import paginate,PageNumberPagination  #分页
from django.shortcuts import get_object_or_404
from rolepermission.models import permission_api
from django.db.utils import IntegrityError
from django.forms.models import model_to_dict

router = Router(tags=["permission"])


#新建权限
@router.post("/create/")
def create_permission(request,data:PermissionIn):
    """
    创建权限
    """
    try:
        per_obj = Permission.objects.create(name=data.name,content_type_id=data.content_type_id,codename=data.codename)
    except IntegrityError:
        return response(error=Error.PERMISSION_CODE_NAME_EXISTS)
    permission_api.objects.create(permission_id =per_obj.id,api_path=data.api_path)
    return response()

#编辑权限
@router.post("/update/{id}/")
def update_permission(request,id:int,data:UpdatePermissionIn):
    api_obj = get_object_or_404(permission_api,id=id)
    per_obj = get_object_or_404(Permission,id=api_obj.permission_id)
    api_obj.api_path = data.api_path
    api_obj.save()
    per_obj.name = data.name
    per_obj.codename = data.codename
    per_obj.content_type_id = data.content_type_id
    per_obj.save()
    return response()

#删除权限
@router.post("/delete/")
def delete_permission(request,data:DeletePermissionIn):
    """
    删除权限
    """
    Permission.objects.get(id=data.permission_id).delete()
    return response()

#获取权限详情
@router.post("/detail/")
def detail_permission(request,data:DetailPermissionIn):
    """
    获取权限详情
    """
    per_obj = Permission.objects.get(id=data.permission_id)
    per_dict =model_to_dict(per_obj)
    per_api_obj = permission_api.objects.get(permission_id=data.permission_id)
    per_dict["api_path"] = per_api_obj.api_path
    return response(result=per_dict)

#获取权限列表
@router.get("/per_list/",response=List[APISchemaOut])
@paginate(CustomPagination)
def get_per_list(request):
    per_obj = permission_api.objects.filter().all()
    return per_obj

#角色添加/更新权限
@router.post("/add/")
def add_role_permission(request,data:RolePermissionIn):
    """
    角色添加权限
    """
    #获取角色对象
    group_obj = Group.objects.get(id=data.group_id)
    group_current_per_obj = group_obj.permissions.values()
    if group_current_per_obj:
        #删除所有权限
         group_obj.permissions.clear()
    per_list = []
    #获取所有权限对象
    obj = Permission.objects.filter().all()
    #获取所有权限id放入列表
    for i in obj:
        per_list.append(i.id)
    print(per_list)
    #判断是否有不存在的权限id，有则抛出异常
    for i in data.permission_id:
        if i not in per_list:
            return response(error=Error.PERMISSION_NOT_EXISTS)
    #添加权限
    for i in data.permission_id:
        per_obj = Permission.objects.get(id=i)
        group_obj.permissions.add(per_obj)
    return response()

#获取角色所有权限
@router.get("/list/{role_id}/")
def get_permission_list(request,role_id:int):
    group_obj = Group.objects.get(id=role_id)
    group_per_obj = group_obj.permissions.values()
    list_resp = []
    if group_per_obj:
        #获取权限列表对象
        per_obj = Permission.objects.filter(content_type_id=13).all()
        for i in range(0,len(per_obj)):
            per_dict = model_to_dict((list(per_obj)[i]))
            api_per_id = per_dict["id"]
            api_per_obj = permission_api.objects.get(permission_id=api_per_id)
            #给权限列表默人无权限字段为False
            per_dict["has_per"] = False
            per_dict["api_path"] = api_per_obj.api_path
            #循环角色拥有的权限列表
            for j in range(0,len(group_per_obj)):
                group_per_dict = list(group_per_obj)[j]
                #如果权限为true跳出内循环
                if per_dict["has_per"] == True:
                    break
                #如果权限为False，且拥有相同的权限ID，权限赋予true
                if  group_per_dict["id"] == per_dict["id"]:
                    per_dict["has_per"] = True
                    break
            #每次循环将字典结果添加到新的列表
            list_resp.append(per_dict)
        return response(result=list_resp)
    else:
        per_obj = Permission.objects.filter(content_type_id=13).all()
        for i in range(0,len(per_obj)):
            per_dict = model_to_dict((list(per_obj)[i]))
            api_per_id = per_dict["id"]
            api_per_obj = permission_api.objects.get(permission_id=api_per_id)
            #给权限列表默人无权限字段为False
            per_dict["api_path"] = api_per_obj.api_path
            per_dict["has_per"] = False
            list_resp.append(per_dict)
        return response(result=list_resp)

