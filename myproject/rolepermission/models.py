from django.db import models
from django.contrib.auth.models import Group,User,Permission


class permission_api(models.Model):
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    api_path = models.CharField("api", max_length=255,default="")

    class Meta:
        default_permissions = ()

#菜单列表
class permission_menu(models.Model):
    title = models.CharField("菜单名",max_length=20,default="")
    path = models.CharField("路径名",max_length=100,default="")
    component = models.CharField("组件",max_length=80,default="")
    icon = models.CharField("icon名",max_length=20,default="")
    parent_id =models.IntegerField("父节点ID，默认为0",null=False)
    hidden = models.BooleanField("是否隐藏",default=False)
    is_delete = models.IntegerField("是否删除，默认为0",default=0)

    class Meta:
        default_permissions = ()

    def __str__(self):
        return self.title

#角色关联的菜单
class permission_role_menu(models.Model):
    role =models.ForeignKey(Group,null=False,on_delete=models.CASCADE)
    menu = models.ForeignKey(permission_menu,null=False,on_delete=models.CASCADE)

    class Meta:
        default_permissions = ()
        unique_together = ("role", "menu")