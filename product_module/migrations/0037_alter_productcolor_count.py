# Generated by Django 4.1.7 on 2023-06-10 14:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0036_productcolor_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcolor',
            name='count',
            field=models.IntegerField(verbose_name='تعداد رنگ موجود برای محصول'),
        ),
    ]