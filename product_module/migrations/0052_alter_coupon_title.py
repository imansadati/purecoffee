# Generated by Django 4.1.7 on 2023-11-01 09:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0051_coupon_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='title',
            field=models.CharField(max_length=100, verbose_name='عنوان'),
        ),
    ]
