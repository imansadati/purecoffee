# Generated by Django 4.1.7 on 2023-06-10 17:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0039_alter_productcolor_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='availability_count',
            field=models.PositiveIntegerField(verbose_name='تعداد موجودی محصول'),
        ),
    ]