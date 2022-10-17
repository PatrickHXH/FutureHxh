from ninja import  NinjaAPI
from users.api import router as users_router
from reports.apis.report_api import router as reports_router
from reports.apis.email_api import router as emails_router
from reports.apis.project_api import  router as projects_router
from ninja.security import HttpBearer
from myproject.common import TokenMethod


# class OverdueToken(Exception):
#     """过期的token"""
#     pass
class InvalidToken(Exception):
    """无效token"""
    pass

class GlobalAuth(HttpBearer):
    def authenticate(self, request,token):
        bool = TokenMethod.check_token(token)
        if bool == False:
            raise InvalidToken
        else:
            return token

api = NinjaAPI(auth=GlobalAuth())
# api = NinjaAPI()

# 自定义异常，改变出现错误时返回值
# @api.exception_handler(OverdueToken)
# def on_overdue_token(request, exc):
#     """过期token返回类型 """
#     return api.create_response(request, {"detail": "Overdue session supplied"}, status=402)

@api.exception_handler(InvalidToken)
def on_overdue_token(request, exc):
    """过期token返回类型 """
    return api.create_response(request, {"detail": "Overdue token supplied"}, status=402)

api.add_router("/users/", users_router)
api.add_router("/reports/", reports_router)
api.add_router("/emails/", emails_router)
api.add_router("/projects/", projects_router)