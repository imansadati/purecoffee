# Generated by Django 4.1.7 on 2023-05-22 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_module', '0015_sitesettingcategory'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesettingcategory',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='فعال / غیرفعال'),
        ),
    ]