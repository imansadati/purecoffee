# Generated by Django 4.1.7 on 2023-06-10 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0038_productcolor_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcolor',
            name='count',
            field=models.PositiveIntegerField(verbose_name='تعداد رنگ موجود برای محصول'),
        ),
    ]
