# Generated by Django 4.1.7 on 2023-10-30 09:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('order_module', '0033_remove_order_transaction'),
        ('wallet_module', '0017_remove_transaction_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='transaction',
            name='order',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='order_module.order', verbose_name='سبد خرید'),
        ),
    ]