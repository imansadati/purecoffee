# Generated by Django 4.1.7 on 2023-10-14 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article_module', '0008_toparticle'),
    ]

    operations = [
        migrations.AddField(
            model_name='toparticle',
            name='short_description',
            field=models.CharField(default=None, max_length=120, verbose_name='توضیحات کوتاه'),
        ),
    ]