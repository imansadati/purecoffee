# Generated by Django 4.1.7 on 2023-03-21 13:07

import colorfield.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0005_remove_product_is_delete'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='color',
        ),
        migrations.CreateModel(
            name='ProductColor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, verbose_name='نام رنگ')),
                ('color', colorfield.fields.ColorField(default='#ffffff', image_field=None, max_length=18, samples=None, verbose_name='رنگ محصول')),
                ('is_active', models.BooleanField(default=False, verbose_name='فعال / غیرفعال')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='product_module.product', verbose_name='محصول')),
            ],
            options={
                'verbose_name': 'رنگ محصول',
                'verbose_name_plural': 'رنگ های محصولات',
            },
        ),
    ]