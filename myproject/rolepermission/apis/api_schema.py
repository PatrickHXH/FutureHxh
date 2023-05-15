from ninja import Schema
from enum import Enum
from typing import List, Any


class RoleIn(Schema):
    name: str


class RoleListOut(Schema):
    id: int
    name: str


class DeleteRoleIn(Schema):
    id: int


class RolePermissionIn(Schema):
    permission_id: List
    group_id: int


class RolePermissionOut(Schema):
    id: int
    name: str
    content_type_id: int
    codename: str


class PermissionIn(Schema):
    codename: str
    name: str
    api_path: str
    content_type_id: int


class UpdatePermissionIn(Schema):
    codename: str
    name: str
    api_path: str
    content_type_id: int


class DeletePermissionIn(Schema):
    permission_id: int


class DetailPermissionIn(Schema):
    permission_id: int


class PermissionSchema(Schema):
    id: int
    content_type_id:int
    codename: str
    name: str


class APISchemaOut(Schema):
    id: int
    api_path: str
    permission: PermissionSchema = None


class APISchemaIn(Schema):
    id: int
    api_path: str
    name: str
    codename: str


class addRoleIn(Schema):
    group_id: int
    user_id: List


class MenuIn(Schema):
    path: str
    title: str
    component:str
    icon: str=None
    hidden:str
    parent_id: int


class roleMenu(Schema):
    role_id:int
    menu_list:List

class userIn(Schema):
    token:str