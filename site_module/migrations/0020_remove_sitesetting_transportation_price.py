# Generated by Django 4.1.7 on 2023-05-27 16:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('site_module', '0019_sitesetting_transportation_price'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='sitesetting',
            name='transportation_price',
        ),
    ]