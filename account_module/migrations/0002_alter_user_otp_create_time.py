# Generated by Django 4.1.7 on 2023-05-07 15:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_module', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='otp_create_time',
            field=models.DateTimeField(auto_now=True, verbose_name='تاریخ ایجاد کد یکبار مصرف'),
        ),
    ]
