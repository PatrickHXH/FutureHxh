# Generated by Django 4.0.4 on 2022-10-11 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reports', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='searchreportlog',
            name='report_time',
            field=models.DateField(null=True, verbose_name='报告时间'),
        ),
    ]