from ninja import  NinjaAPI
from users.api import router as users_router
from reports.apis.report_api import router as reports_router
from reports.apis.email_api import router as emails_router
from reports.apis.project_api import  router as projects_router
from scheduled.apis.scheduled_api import router as scheduled_router
from rolepermission.apis.menu_api import router as menu_router
from rolepermission.apis.role_api import router as role_router
from rolepermission.apis.permission_api import router as permisssion_router
from performance.api import  router as performance_router
from audio.apis.delayed_api import router as audio_router
from ninja.security import HttpBearer
from ninja.renderers import BaseRenderer
from myproject.common import TokenMethod,Error
import yaml
import orjson
from django.contrib.auth.models import Group,User,Permission
from rolepermission.models import permission_api
from ninja.parser import Parser
import re
class InvalidToken(Exception):
    """无效token"""
    pass

class NotPermission(Exception):
    """没有权限"""
    pass

class GlobalAuth(HttpBearer):
    def authenticate(self, request,token):
        bool = TokenMethod.check_token(token)
        if bool == False:
            raise InvalidToken
        else:
            # token = request.headers["Authorization"].split(" ")[1]
            username = TokenMethod.get_username(token)
            if username =="admin":
                return token
            else:
                User_obj = User.objects.get(username=username)
                group_perm = User_obj.get_group_permissions()
                api_path = request.get_full_path().split("?")[0]
                api_path = re.match(r'/api/\D*', api_path).group()
                try:
                    api_per_obj = permission_api.objects.get(api_path=api_path)
                    per_obj = Permission.objects.get(id=api_per_obj.permission_id)
                    for i in group_perm:
                        if i.split(".")[1] == per_obj.codename:
                            return token
                    raise NotPermission
                except permission_api.DoesNotExist:
                    raise NotPermission

api = NinjaAPI(auth=GlobalAuth())
# api = NinjaAPI()

@api.exception_handler(InvalidToken)
def on_overdue_token(request, exc):
    """过期token返回类型 """
    return api.create_response(request, {"detail": "Overdue token supplied"}, status=402)

@api.exception_handler(NotPermission)
def not_permission(request, exc):
    """过期token返回类型 """
    return api.create_response(request, {"detail": "无该接口权限"}, status=403)

api.add_router("/users/", users_router)
api.add_router("/reports/", reports_router)
api.add_router("/emails/", emails_router)
api.add_router("/projects/", projects_router)
api.add_router("/scheduled/", scheduled_router)
api.add_router("/rolepermission/", role_router)
api.add_router("/permission/",permisssion_router)
api.add_router("/menu/",menu_router)
api.add_router("/performance/",performance_router)
api.add_router("/audio/",audio_router)