# Generated by Django 4.1.7 on 2023-05-22 17:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0022_product_status_alter_product_description'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='product',
            options={'ordering': ['-status', '-create_date'], 'verbose_name': 'محصول', 'verbose_name_plural': 'محصولات'},
        ),
    ]
