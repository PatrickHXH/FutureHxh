from ninja import Router
from myproject.common import response, Error, TokenMethod
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.models import Group,User,Permission
from rolepermission.apis.api_schema import  RoleIn,RoleListOut,DeleteRoleIn,addRoleIn
from typing import  List,Any
from myproject.pagination import CustomPagination #自定义分页
from ninja.pagination import paginate,PageNumberPagination  #分页
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict
router = Router(tags=["role"])

# 创建角色（添加组）
@router.post("/createrole/")
def create_role(request,data:RoleIn):
    group_obj = Group.objects.all()
    for obj in group_obj:
        if obj.name == data.name:
            return response(result="角色存在")
    Group.objects.create(name=data.name)
    return response()

#获取角色列表
@router.get("/rolelist/",response=List[RoleListOut])
@paginate(CustomPagination)
def get_role_list(request):
    obj = Group.objects.order_by("id").filter().all()
    return obj

#获取角色详情
@router.get("/roledetail/{id}/")
def get_role_detail(request,id:int):
    # obj = Group.objects.get(id=id)
    obj = get_object_or_404(Group,id=id)
    obj_dict = model_to_dict(obj)
    obj_dict.pop("permissions")
    return response(result=obj_dict)

#删除角色
@router.post("/roledelete/")
def role_delete(request,data:DeleteRoleIn):
    try:
        obj_group = get_object_or_404(Group,id=data.id)
    except:
        return response(error=Error.ROLE_NOT_EXISTS)
    user = User.objects.filter().all()
    if user:
        for i in user:
            all_per = i.groups.remove(obj_group)
    Group.objects.filter(id=data.id).delete()
    return response()

#更改角色名
@router.post("/roleupdate/{id}/")
def role_update(request,data:RoleIn,id:int):
    obj = get_object_or_404(Group,id=id)
    for attr,value in data.dict().items():
        setattr(obj,attr,value)
    obj.save()
    return response()

#给用户添加组/角色
@router.post("/addrole/")
def add_role(request,data:addRoleIn):
    #获取组对象
    group_obj = Group.objects.get(id=data.group_id)
    #获取所有用户对象
    user_obj_all =  User.objects.filter().all()
    for i in user_obj_all:
        i.groups.remove(group_obj)
    #获取用户对象
    for i in data.user_id:
        user_obj = User.objects.get(id=i)
        #给用户添加组
        user_obj.groups.add(group_obj)
    return response()

#获取角色关联用户列表
@router.get("/userlist/{group_id}/")
def get_user_list(request,group_id:int):
    user_obj = User.objects.filter().all()
    user_list = []
    for i in user_obj:
        user_all_dict = model_to_dict(i)
        user_dict = {}
        user_dict["id"]  = user_all_dict["id"]
        user_dict["username"] = user_all_dict["username"]
        if user_all_dict["groups"] == []:
            user_dict["is_current_group"] = False
        else:
            for i in user_all_dict["groups"]:
                if i.id == group_id:
                    user_dict["is_current_group"] = True
                    break
                user_dict["is_current_group"] = False
        user_list.append(user_dict)
    return response(result=user_list)
