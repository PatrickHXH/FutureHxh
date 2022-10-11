from ninja import Router
from myproject.common import response, Error
from reports.apis.api_schema import SearchReport,ReaportLogIn,ReaportLogOut
from reports.apis.EamilCommon import email
from reports.models import SearchReportLog
from django.forms.models import model_to_dict
from myproject.pagination import CustomPagination
from ninja.pagination import paginate,PageNumberPagination  #分页
from typing import  List,Any
import datetime

router = Router(tags=["reports"])

#查询最新测试报告
@router.post("/search")
def search_project_report(request,payload:SearchReport):
        source = payload.source
        reportime = payload.reportime
        email_user = payload.email_user
        password = payload.password
        server = payload.server
        #判断报告时间是否符合查询 (只允许查询<=90)
        a = reportime.split("-")
        first = datetime.date(int(a[0]), int(a[1]), int(a[2]))
        #当天日期减90天
        now = datetime.datetime.now()
        offset = datetime.timedelta(days=-90)
        date = (now + offset).strftime("%Y-%m-%d")
        a = date.split("-")
        second = datetime.date(int(a[0]), int(a[1]), int(a[2]))
        if first < second:
                return response(error=Error.SEARCH_REPORT_TIME_BEYOND)
        #解析邮箱
        try:
                result = email.get_reportlist(source,reportime,email_user,password,server)
        except:
                return response(error=Error.USER_OR_PAWD_OR_SERVER_ERROR)
        if result ==[]:
                return response(error=Error.REPORT_LIST_NONE)
        #转换时间格式
        try:
                reportime = datetime.datetime.strptime(reportime, "%Y-%m-%d")
        except:
                return response(error=Error.DATE_FORMAT_ERROR)
        #插入查询记录
        SearchReportLog.objects.create(
                subject=result["Subject"],
                sender=result["From"],
                receive=result["To"],
                text=result["Text"],
                source=source,
                email_id =result["email_id"],
                report_time = reportime
        )
        return response(result=result)

#获取查询记录
@router.post("/searchlog",response=List[ReaportLogOut])
@paginate(CustomPagination)
def search_report_log(request,data:ReaportLogIn):
        source = data.source
        reportime = data.reportime
        if reportime =="":
                obj = SearchReportLog.objects.filter(source=source,report_time__isnull=False).order_by("-create_time")
        else:
                obj = SearchReportLog.objects.filter(source=source,report_time=reportime).order_by("-create_time")
        return obj