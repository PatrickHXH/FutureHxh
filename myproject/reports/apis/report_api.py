from ninja import Router
from myproject.common import response, Error
from reports.apis.api_schema import SearchReportIn,DownloadReportIn,SearchReportLogOut,ProjectSchema
from reports.apis.EamilCommon import email
from reports.models import EmailManage,ProjectManage,SearchReportLog
from django.forms.models import model_to_dict
from myproject.pagination import CustomPagination
from ninja.pagination import paginate,PageNumberPagination  #分页
from typing import  List,Any
from myproject.settings import REPORT_DIR
from django.shortcuts import get_object_or_404
import datetime
import os

router = Router(tags=["reports"])


#查询当天最新测试报告
@router.post("/search/")
def search_project_report(request,data:SearchReportIn):
        project_id = data.project_id
        email_id = data.email_id
        project_obj = get_object_or_404(ProjectManage,id=project_id)
        email_obj = get_object_or_404(EmailManage, id=email_id)
        #获取当天时间
        reportime = datetime.datetime.now().strftime( "%Y-%m-%d")
        update_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #解析邮箱
        try:
                result = email.get_reportlist(project_obj.keyword,reportime,email_obj.email,email_obj.code,email_obj.server)
        except:
                return response(error=Error.USER_OR_PAWD_OR_SERVER_ERROR)
        if result == [] or result == None:
                return response(error=Error.REPORT_LIST_NONE)
        email_code = result["email_code"]
        #下载附件
        # obj = get_object_or_404(SearchReportLog,project_id=project_id)
        msg_origin = email.get_origin_text(email_code,email_obj.email,email_obj.code,email_obj.server)         #邮件原文
        att_result = email.save_att_file(msg_origin,REPORT_DIR)         #下载附件
        if att_result is not None:
                report_dir = os.path.join("/backendstatic/reports/",att_result)
                print(report_dir)
        else:
                return response(error=Error.EMAIL_ATT_NOT_EXISTS)
        #项目查询到报告后有没有查询记录，有则更新，没有则新建
        obj = SearchReportLog.objects.filter(project_id=project_id)
        if obj.count() == 0:
                # 插入查询记录
                obj = SearchReportLog.objects.create(
                        subject=result["Subject"],
                        sender=result["From"],
                        receive=result["To"],
                        text=result["Text"],
                        project_id=project_id,
                        report_time = reportime,
                        update_time = update_time,
                        create_time=update_time
                )
                obj.report_dir = report_dir
                obj.save()
        else:
                obj = SearchReportLog.objects.get(project_id=project_id)
                #更新查询记录
                SearchReportLog.objects.filter(id=obj.id).update(
                        subject=result["Subject"],
                        sender=result["From"],
                        receive=result["To"],
                        text=result["Text"],
                        report_time=reportime,
                        project_id=project_id,
                        report_dir=report_dir,
                        update_time=update_time
                )

        return response()

#获取查询记录列表
@router.get("/list/",response=List[SearchReportLogOut])
@paginate(CustomPagination)
def reportlog_list(request):
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        print(today)
        obj =SearchReportLog.objects.filter().all()
        for i in obj:
                if str(i.report_time) == today:
                        i.lastest = True
                        i.save()
                else:
                        i.lastest = False
                        i.save()
        return obj

#下载测试报告
# @router.post("/download/")
# def report_download(request, data: DownloadReportIn):
#         email_code = data.email_code
#         email_id = data.email_id
#         email_obj = get_object_or_404(EmailManage, id=email_id)
#         #邮件原文
#         msg_origin = email.get_origin_text(email_code,email_obj.email,email_obj.code,email_obj.server)
#         #下载附件
#         result = email.save_att_file(msg_origin,REPORT_DIR)
#         if result is not None:
#                 report_dir = os.path.join("http://localhost:8000/static/reports/",result)
#                 return response(result=report_dir)
#         else:
#                 return response(result=None)
