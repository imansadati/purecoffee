# Generated by Django 4.1.7 on 2023-10-30 11:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_module', '0036_alter_order_transaction_amount'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='transaction_amount',
            field=models.BigIntegerField(blank=True, null=True, verbose_name='مبلغ تراکنش کیف پول'),
        ),
    ]
