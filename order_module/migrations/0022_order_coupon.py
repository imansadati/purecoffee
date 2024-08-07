# Generated by Django 4.1.7 on 2023-10-01 16:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0050_remove_coupon_used_count'),
        ('order_module', '0021_alter_wholesale_phone_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='coupon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='product_module.coupon', verbose_name='کد تخفیف'),
        ),
    ]
