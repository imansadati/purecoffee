# Generated by Django 4.1.7 on 2023-10-30 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet_module', '0022_alter_transaction_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='amount',
            field=models.IntegerField(default=0, verbose_name='مبلغ تراکنش'),
        ),
    ]
