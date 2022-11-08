from myproject.common import response, Error
from reports.models import ProjectManage,EmailManage
from reports.apis.ReportsCommon import SearchReport


def Search_Report():
    obj_project = ProjectManage.objects.filter()
    obj_email = EmailManage.objects.filter()
    if obj_project and obj_email:
        for j in obj_email:
            for i in obj_project:
                    SearchReport(i.id,j.id)
    else:
            return response(error=Error.PROJECT_OR_EMAIL_NOT_EXISTS)
    return response()
