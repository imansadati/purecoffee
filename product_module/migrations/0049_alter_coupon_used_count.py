# Generated by Django 4.1.7 on 2023-10-01 07:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0048_coupon_used_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coupon',
            name='used_count',
            field=models.IntegerField(verbose_name='تعداد استفاده'),
        ),
    ]
