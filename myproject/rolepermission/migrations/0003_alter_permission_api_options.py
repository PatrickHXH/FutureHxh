# Generated by Django 4.0.6 on 2022-12-19 15:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rolepermission', '0002_rename_permission_id_permission_api_permission'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='permission_api',
            options={'default_permissions': ()},
        ),
    ]
