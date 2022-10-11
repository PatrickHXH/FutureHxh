from django.db import models
import datetime

class SearchReportLog(models.Model):
    subject = models.CharField("测试报告名称",max_length=50,null=True)
    sender = models.CharField("发送人",max_length=50,null=True)
    receive = models.CharField("接收人",max_length=50,null=True)
    text = models.TextField("正文",null=True)
    source = models.CharField("来源", max_length=50,null=True)
    email_id = models.IntegerField("邮件id",null=True)
    report_time = models.DateField("报告时间", null=True)
    update_time = models.DateTimeField("更新时间",auto_now=True)
    create_time = models.DateTimeField("创建时间",auto_now_add=True)

    def __str__(self):
        return self.subject

class EmailManage(models.Model):
    email = models.CharField("邮箱", max_length=50,null=False)
    code = models.CharField("邮箱授权码",max_length=50,null=False)
    server = models.CharField("服务器地址",max_length=50,null=False)
    is_delete = models.IntegerField("删除",default=0)
    update_time = models.DateTimeField("更新时间",auto_now=True)
    create_time = models.DateTimeField("创建时间",auto_now_add=True)

    def __str__(self):
        return self.email



