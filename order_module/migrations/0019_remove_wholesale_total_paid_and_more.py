# Generated by Django 4.1.7 on 2023-08-28 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order_module', '0018_alter_wholesale_statement_alter_wholesale_total_paid'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wholesale',
            name='total_paid',
        ),
        migrations.AddField(
            model_name='wholesale',
            name='total_amount_paid',
            field=models.PositiveBigIntegerField(default=0, verbose_name='کل مبلغ پرداخت شده'),
        ),
        migrations.AddField(
            model_name='wholesale',
            name='total_amount_payable',
            field=models.PositiveBigIntegerField(default=0, verbose_name='کل مبلغ قابل پرداخت'),
        ),
    ]