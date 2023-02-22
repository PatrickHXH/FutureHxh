from ninja import Router
from myproject.common import response, Error, TokenMethod
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.models import Group,User,Permission
from rolepermission.models import permission_menu,permission_role_menu
from rolepermission.apis.api_schema import MenuIn,roleMenu,userIn
from typing import  List,Any
from myproject.pagination import CustomPagination #自定义分页
from ninja.pagination import paginate,PageNumberPagination  #分页
from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict

router = Router(tags=["menu"])

####################菜单相关操作###############################
# 新建菜单
@router.post("/create/")
def create_menu(request,data:MenuIn):
    if data.component == "Layout":
        permission_menu.objects.create(
            title=data.title,
            path=data.path,
            icon=data.icon,
            parent_id=0,
            hidden=data.hidden,
            component=data.component
        )
    else:
        permission_menu.objects.create(
            title=data.title,
            path=data.path,
            icon=data.icon,
            parent_id=data.parent_id,
            hidden=data.hidden,
            component=data.component
        )
    return response()

#删除菜单
@router.post("/delete/{id}/")
def delete_menu(request,id:int):
    menu_obj = permission_menu.objects.get(id=id)
    menu_obj.is_delete=1
    menu_obj.save()
    return response()

#菜单详情
@router.get("/detail/{id}/")
def detail_menu(request,id:int):
    menu_obj = permission_menu.objects.get(id=id)
    menu_dict = model_to_dict(menu_obj)
    if menu_obj.parent_id !=0:
        menu_parent_obj = permission_menu.objects.get(id=menu_obj.parent_id)
        menu_dict["parent_title"] =menu_parent_obj.title
    else:
        menu_dict["parent_title"] =""
    return  response(result=menu_dict)

#编辑菜单
@router.post("/update/{id}/")
def update_menu(request,id:int,data:MenuIn):
    obj = get_object_or_404(permission_menu, id=id)
    if id==data.parent_id:
        return response(error=Error.MENU_ID_AND_PARENT_ID_IS_SAME)
    print(data.dict().items())
    for attr,value in data.dict().items():
        setattr(obj,attr,value)
    obj.save()
    return response()

#判断节点是否有子节点
def children_node(all_nodes,current_node):
    for i in all_nodes:
        if current_node["id"] == i["parent_id"]:
            return True
    return False

#递归，将子节点放入父节点，找出当前节点所有子节点并返回
def tree_node(all_nodes,current_node):
    for i in all_nodes:
        if current_node["id"] == i["parent_id"]:
            current_node["children"].append(i)
            tree_node(all_nodes,i)
    return current_node

#菜单列表
@router.get("/list/")
def list_menu(request):
    menu_obj = permission_menu.objects.filter(is_delete=0)
    list = []
    for i in menu_obj:
        list.append({
            "id": i.id,
            "path": i.path,
            "title": i.title,
            "icon": i.icon,
            "component": i.component,
            "hidden":i.hidden,
            "children": [],
            "parent_id": i.parent_id,
        })
    data = []
    for i in list:
        # 判断该节点是否有子节点，用true和False返回
        is_children = children_node(list, i)
        if (i["parent_id"] == 0) and (is_children is False):
            data.append(i)
        elif (i["parent_id"] == 0) and (is_children is True):
            ret = tree_node(list, i)
            data.append(ret)
    return response(result=data)



######################角色菜单相关操作##############################
#给角色授权菜单
@router.post("/role/update/")
def save_role_menu(request,data:roleMenu):
    role_obj = Group.objects.filter(id=data.role_id)  #获取角色对象
    role_menu_obj = permission_role_menu.objects.filter(role_id=data.role_id)  #获取角色菜单权限对象

    if role_obj.count() == 0:
        return response(error=Error.ROLE_NOT_EXISTS)
    role_menu_obj.delete()
    for i in data.menu_list:
            permission_role_menu.objects.update_or_create(role_id=data.role_id,menu_id=i)
    return response(result="已添加或更新")

# 获取角色菜单列表
@router.get("/rolelist/{role_id}/")
def list_role_menu(request,role_id:int):
    role_menu_obj = permission_role_menu.objects.filter(role_id=role_id)   #获取角色菜单权限对象
    menu_obj = permission_menu.objects.filter(is_delete=0)   #获取菜单对象
    list = []
    #判断角色菜单权限是否为0，若为0，所有权限均为False
    if role_menu_obj.count() == 0:
        for i in menu_obj:
            list.append({
                "id": i.id,
                "path": i.path,
                "title": i.title,
                "icon": i.icon,
                "cmp": i.component,
                "parent_id": i.parent_id,
                "has_per": False,
                "children": [],
            })
    else:
        #角色存在菜单权限，判断每个菜单的权限并赋予True
        for i in menu_obj:
            has_per = False
            for j in role_menu_obj:
                if i.id == j.menu_id:
                    has_per = True
                    break
            list.append({
                        "id": i.id,
                        "path": i.path,
                         "title": i.title,
                         "icon":i.icon,
                         "cmp":i.component,
                        "parent_id": i.parent_id,
                        "has_per": has_per,
                        "children": [],
                         })
    data = []
    #递归，返回树形结构
    for i in list:
        # 判断该节点是否有子节点，用true和False返回
        is_children = children_node(list, i)
        if (i["parent_id"] == 0) and (is_children is False):
            data.append(i)
        elif (i["parent_id"] == 0) and (is_children is True):
            ret = tree_node(list, i)
            data.append(ret)
    return response(result=data)


#根据token获取用户菜单
@router.post("/user/",auth=None)
def get_user_menu(request,data:userIn):
    #获取用户名称
    username = TokenMethod.get_username(data.token)
    #获取用户对象
    user_obj = User.objects.get(username=username)
    #查看用户所在组
    group_obj = user_obj.groups.values()
    menu_list = []
    for i in group_obj:
        #i为用户的角色，有了用户角色可以查找该角色有哪些权限
        role_menu_obj = permission_role_menu.objects.filter(role_id=i["id"])
        for j in role_menu_obj:
            if j.menu_id in menu_list:
                continue
            else:
                menu_list.append(j.menu_id)
    print(menu_list)
    list = []
    for i in menu_list:
        menu_obj = permission_menu.objects.filter(id=i,is_delete=0) #返回查询集合，所有需循环
        for k in menu_obj:
            list.append({
                "id": k.id,
                "path": k.path,
                "title": k.title,
                "icon": k.icon,
                "cmp": k.component,
                "hidden":k.hidden,
                "parent_id": k.parent_id,
                "children": [],
            })
    data = []
    # 递归，返回树形结构
    for i in list:
        # 判断该节点是否有子节点，用true和False返回
        is_children = children_node(list, i)
        if (i["parent_id"] == 0) and (is_children is False):
            data.append(i)
        elif (i["parent_id"] == 0) and (is_children is True):
            ret = tree_node(list, i)
            data.append(ret)
    return response(result=data)