import datetime

from django.db import models
from django.db.backends.sqlite3.base import DatabaseFeatures # 关键设置
DatabaseFeatures.supports_microsecond_precision = False # 关键设置

class EmailManage(models.Model):
    email = models.CharField("邮箱", max_length=50,null=False)
    code = models.CharField("邮箱授权码",max_length=50,null=False)
    server = models.CharField("服务器地址",max_length=50,null=False)
    update_time = models.DateTimeField("更新时间",auto_now=True)
    create_time = models.DateTimeField("创建时间",auto_now_add=True)


    def __str__(self):
        return self.email

class ProjectManage(models.Model):
    name = models.CharField("项目名称", max_length=50,null=False)
    keyword = models.CharField("关键字", max_length=50,default="")
    update_time = models.DateTimeField("更新时间",auto_now=True)
    create_time = models.DateTimeField("创建时间",auto_now_add=True)

    def __str__(self):
        return self.project

class SearchReportLog(models.Model):
    project = models.ForeignKey(ProjectManage, on_delete=models.CASCADE)
    subject = models.CharField("测试报告名称",max_length=50,null=True)
    sender = models.CharField("发送人",max_length=50,null=True)
    receive = models.CharField("接收人",max_length=50,null=True)
    text = models.TextField("正文",null=True)
    report_time = models.DateField("报告时间", null=True)
    report_dir = models.CharField("报告路径", max_length=500,null=True)
    lastest =models.BooleanField("是否最新",default=True)
    existfail = models.BooleanField("报告是否存在错误",default=False)
    update_time = models.DateTimeField("更新时间",auto_now=True)
    create_time = models.DateTimeField("创建时间",auto_now_add=True)

    def __str__(self):
        return self.subject




