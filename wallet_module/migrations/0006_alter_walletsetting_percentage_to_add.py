# Generated by Django 4.1.7 on 2023-09-05 11:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wallet_module', '0005_alter_wallet_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='walletsetting',
            name='percentage_to_add',
            field=models.IntegerField(default=5, verbose_name='درصد اضافه شدن به سبد خرید'),
        ),
    ]