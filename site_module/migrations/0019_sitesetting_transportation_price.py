# Generated by Django 4.1.7 on 2023-05-27 15:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_module', '0018_alter_sitesettingcategory_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesetting',
            name='transportation_price',
            field=models.CharField(choices=[('free', 'رایگان'), ('30', '30')], default=20, max_length=200, verbose_name='قیمت حمل و نقل محصول'),
        ),
    ]