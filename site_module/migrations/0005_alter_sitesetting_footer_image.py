# Generated by Django 4.1.7 on 2023-04-02 14:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_module', '0004_sitesetting_footer_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sitesetting',
            name='footer_image',
            field=models.ImageField(upload_to='images/site_setting', verbose_name='تصویر پس زمینه فوتر سایت'),
        ),
    ]