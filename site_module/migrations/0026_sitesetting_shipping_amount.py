# Generated by Django 4.1.7 on 2023-11-02 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_module', '0025_alter_sitebanner_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='sitesetting',
            name='shipping_amount',
            field=models.IntegerField(default=0, verbose_name='هزینه حمل و نقل'),
        ),
    ]