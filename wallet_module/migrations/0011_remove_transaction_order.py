# Generated by Django 4.1.7 on 2023-10-23 16:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wallet_module', '0010_alter_transaction_order'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='transaction',
            name='order',
        ),
    ]
