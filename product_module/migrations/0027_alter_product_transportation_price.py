# Generated by Django 4.1.7 on 2023-05-27 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0026_alter_product_transportation_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='transportation_price',
            field=models.PositiveBigIntegerField(verbose_name='قیمت حمل و نقل محصول'),
        ),
    ]
