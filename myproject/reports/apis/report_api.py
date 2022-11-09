from ninja import Router
from myproject.common import response, Error
from reports.apis.api_schema import SearchReportIn,DownloadReportIn,SearchReportLogOut,ProjectSchema
from reports.apis.EamilCommon import email
from reports.models import EmailManage,ProjectManage,SearchReportLog
from reports.apis.ReportsCommon import SearchReport
from django.forms.models import model_to_dict
from myproject.pagination import CustomPagination
from ninja.pagination import paginate,PageNumberPagination  #分页
from typing import  List,Any
from myproject.settings import REPORT_DIR
from django.shortcuts import get_object_or_404
from reports.apis.HtmlCommon import Exist_Fail
from myproject.settings import BASE_DIR
import datetime
import os

router = Router(tags=["reports"])


#查询当天最新测试报告
@router.post("/search/")
def search_project_report(request,data:SearchReportIn):
        project_id = data.project_id
        email_id = data.email_id

        msg = SearchReport(project_id,email_id)
        return msg

#获取查询记录列表
@router.get("/list/",response=List[SearchReportLogOut])
@paginate(CustomPagination)
def reportlog_list(request):
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        print(today)
        obj =SearchReportLog.objects.filter().all()
        for i in obj:
                if str(i.report_time) == today and i.lastest ==1:
                        continue
                if str(i.report_time) == today and i.lastest == 0:
                        i.lastest = True
                        i.save()
                if str(i.report_time) !=today and i.lastest == 1:
                        i.lastest = False
                        i.save()
                if str(i.report_time) != today and i.lastest == 0:
                        continue
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
