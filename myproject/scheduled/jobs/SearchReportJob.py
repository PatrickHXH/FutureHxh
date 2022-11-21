from myproject.common import response, Error
from reports.models import ProjectManage,EmailManage,SearchReportLog
from reports.apis.ReportsCommon import SearchReport
import datetime

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

def Search_Report_lastest():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    print(today)
    obj_log = SearchReportLog.objects.filter().all()
    if obj_log:
        for k in obj_log:
            if str(k.report_time) == today and k.lastest == 1:
                continue
            if str(k.report_time) == today and k.lastest == 0:
                k.lastest = True
                k.save()
            if str(k.report_time) != today and k.lastest == 1:
                k.lastest = False
                k.save()
            if str(k.report_time) != today and k.lastest == 0:
                continue
    else:
        return  response(error=Error.PROJECT_OR_EMAIL_NOT_EXISTS)
    return response()