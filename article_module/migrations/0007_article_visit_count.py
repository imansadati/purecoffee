# Generated by Django 4.1.7 on 2023-07-10 10:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article_module', '0006_alter_article_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='visit_count',
            field=models.IntegerField(default=0, verbose_name='تعداد بازدید'),
        ),
    ]
