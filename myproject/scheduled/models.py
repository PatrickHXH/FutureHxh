from django_apscheduler.models import DjangoJob
from django.db import models

class DjangoJobExtend(models.Model):
    job = models.ForeignKey(DjangoJob,on_delete=models.CASCADE)
    describe = models.TextField("描述",null=False)
    excutefun = models.CharField("执行函数",max_length=50,null=False,default="")
    trigger = models.CharField("触发类型",max_length=50,null=False,default="")
    crontab = models.CharField("触发时间", max_length=50, null=False, default="")
    state =models.BooleanField("是否开启",default=1)

    def __str__(self):
        return self.describe