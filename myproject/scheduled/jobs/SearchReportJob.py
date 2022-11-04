from myproject.common import response, Error
from reports.models import ProjectManage
from reports.apis.ReportsCommon import SearchReport


def Search_Report():
    obj = ProjectManage.objects.filter()
    if obj:
            for i in obj:
                    SearchReport(i.id,4)
    else:
            return response(error=Error.PROJECT_ID_NOT_EXISTS)
    return response()
