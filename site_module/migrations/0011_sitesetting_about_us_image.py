# Generated by Django 4.1.7 on 2023-04-09 12:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_module', '0010_remove_sitesetting_footer_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesetting',
            name='about_us_image',
            field=models.ImageField(blank=True, null=True, upload_to='images/site_setting', verbose_name='تصویر صفحه درباره ما'),
        ),
    ]
