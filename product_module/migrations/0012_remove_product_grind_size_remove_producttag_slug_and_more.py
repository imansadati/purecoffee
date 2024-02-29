# Generated by Django 4.1.7 on 2023-03-25 09:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product_module', '0011_alter_productgrind_options_remove_product_grind_size_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='grind_size',
        ),
        migrations.RemoveField(
            model_name='producttag',
            name='slug',
        ),
        migrations.AddField(
            model_name='producttag',
            name='url_title',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='عنوان تگ در url'),
        ),
        migrations.DeleteModel(
            name='ProductGrind',
        ),
    ]
