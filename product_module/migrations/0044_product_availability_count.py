# Generated by Django 4.1.7 on 2023-06-13 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0043_remove_product_grind_product_grind'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='availability_count',
            field=models.PositiveIntegerField(blank=True, help_text='به غیر از رنگ ها', null=True, verbose_name='تعداد موجودی محصول'),
        ),
    ]