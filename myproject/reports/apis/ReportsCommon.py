from reports.apis.EamilCommon import email
from myproject.settings import BASE_DIR,REPORT_DIR
from reports.models import EmailManage,ProjectManage,SearchReportLog
from myproject.common import response, Error
from django.shortcuts import get_object_or_404
from reports.apis.HtmlCommon import Exist_Fail
import datetime
import os

def SearchReport(project_id:int,email_id:int):
    project_obj = get_object_or_404(ProjectManage, id=project_id)
    email_obj = get_object_or_404(EmailManage, id=email_id)
    # 获取当天时间
    reportime = datetime.datetime.now().strftime("%Y-%m-%d")
    update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    # 解析邮箱
    try:
        result = email.get_reportlist(project_obj.keyword, reportime, email_obj.email, email_obj.code, email_obj.server)
    except:
        return response(error=Error.USER_OR_PAWD_OR_SERVER_ERROR)
    if result == [] or result == None:
        return response(error=Error.REPORT_LIST_NONE)
    #获取邮件id
    email_code = result["email_code"]
    # 下载附件
    # obj = get_object_or_404(SearchReportLog,project_id=project_id)
    msg_origin = email.get_origin_text(email_code, email_obj.email, email_obj.code, email_obj.server)  # 邮件原文
    att_result = email.save_att_file(msg_origin, REPORT_DIR)  # 下载附件
    if att_result is not None:
        report_dir = os.path.join("/backendstatic/reports/", att_result)
        print(report_dir)
    else:
        return response(error=Error.EMAIL_ATT_NOT_EXISTS)
    # 查询报告有没有存在错误用例
    TEST_REPORT = os.path.join(BASE_DIR, "backendstatic", "reports", att_result)
    ret = Exist_Fail(TEST_REPORT)
    # 项目查询到报告后有没有查询记录，有则更新，没有则新建
    obj = SearchReportLog.objects.filter(project_id=project_id)
    if obj.count() == 0:
        # 插入查询记录
        obj = SearchReportLog.objects.create(
            subject=result["Subject"],
            sender=result["From"],
            receive=result["To"],
            text=result["Text"],
            project_id=project_id,
            report_time=reportime,
            existfail=ret,
            lastest=1,
            update_time=update_time,
            create_time=update_time
        )
        obj.report_dir = report_dir
        obj.save()
    else:
        obj = SearchReportLog.objects.get(project_id=project_id)
        # 更新查询记录
        SearchReportLog.objects.filter(id=obj.id).update(
            subject=result["Subject"],
            sender=result["From"],
            receive=result["To"],
            text=result["Text"],
            report_time=reportime,
            existfail=ret,
            project_id=project_id,
            report_dir=report_dir,
            lastest=1,
            update_time=update_time
        )
    return  response()