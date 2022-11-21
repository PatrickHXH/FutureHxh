from myproject.common import response, Error
from reports.models import ProjectManage,EmailManage,SearchReportLog
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
    obj = SearchReportLog.objects.filter().all()
    for i in obj:
        if str(i.report_time) == today and i.lastest == 1:
            continue
        if str(i.report_time) == today and i.lastest == 0:
            i.lastest = True
            i.save()
        if str(i.report_time) != today and i.lastest == 1:
            i.lastest = False
            i.save()
        if str(i.report_time) != today and i.lastest == 0:
            continue
    return response()
