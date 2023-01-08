from django.db import models
from django.contrib.auth.models import Group,User,Permission


class permission_api(models.Model):
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    api_path = models.CharField("api", max_length=255,default="")

    class Meta:
        default_permissions = ()