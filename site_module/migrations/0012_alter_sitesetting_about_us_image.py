# Generated by Django 4.1.7 on 2023-04-09 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_module', '0011_sitesetting_about_us_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesetting',
            name='about_us_image',
            field=models.ImageField(upload_to='images/site_setting', verbose_name='تصویر صفحه درباره ما'),
        ),
    ]
