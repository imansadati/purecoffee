# Generated by Django 4.1.7 on 2023-07-10 18:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_module', '0007_user_full_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='full_name',
            field=models.CharField(max_length=120, verbose_name='نام و نام خانوادگی'),
        ),
    ]
