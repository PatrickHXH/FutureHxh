from django_apscheduler.models import DjangoJob
from django.db import models

class DjangoJobExtend(models.Model):
    job = models.ForeignKey(DjangoJob,on_delete=models.CASCADE)
    describe = models.TextField("描述",null=True)

    def __str__(self):
        return self.describe