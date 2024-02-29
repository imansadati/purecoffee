# Generated by Django 4.1.7 on 2023-10-25 08:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order_module', '0028_remove_orderdetail_payable_amount_and_more'),
        ('wallet_module', '0011_remove_transaction_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='order',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='order_module.order', verbose_name='سبد خرید'),
        ),
    ]