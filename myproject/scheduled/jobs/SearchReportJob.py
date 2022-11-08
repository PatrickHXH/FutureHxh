from myproject.common import response, Error
from reports.models import ProjectManage,EmailManage
from reports.apis.ReportsCommon import SearchReport


def Search_Report():
    obj = ProjectManage.objects.filter()
    obj_email = EmailManage.objects.get(email="huangxh@joysim.cn")
    if obj:
            for i in obj:
                    SearchReport(i.id,obj_email.id)
    else:
            return response(error=Error.PROJECT_ID_NOT_EXISTS)
    return response()
