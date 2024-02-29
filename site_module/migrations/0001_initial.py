# Generated by Django 4.1.7 on 2023-04-01 08:25

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SiteSetting',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('site_name', models.CharField(max_length=30, verbose_name='نام سایت')),
                ('site_name_title', models.CharField(max_length=150, verbose_name='نام سایت در گوگل')),
                ('site_description', models.TextField(verbose_name='درباره سایت')),
                ('short_description', models.CharField(max_length=150, verbose_name='توضیحات کوتاه سایت')),
                ('products_count', models.IntegerField(verbose_name='تعداد محصولات')),
                ('customer_count', models.IntegerField(verbose_name='تعداد مشتریان')),
                ('phone_number', models.IntegerField(verbose_name='شماره تماس سایت')),
                ('email', models.EmailField(max_length=254, verbose_name='آدرس ایمیل')),
                ('site_icon', models.ImageField(upload_to='images/site_setting', verbose_name='لوگو کوچک سایت')),
                ('copyright', models.CharField(max_length=150, verbose_name='متن کپی رایت')),
                ('newletter_text', models.CharField(max_length=200, verbose_name='متن خبر نامه سایت')),
                ('why_pure_text', models.TextField(verbose_name='متن چرا ما را باید انتخاب کنید')),
                ('is_main_setting', models.BooleanField(default=True, verbose_name='تنظیم به عنوان تنظیمات اصلی')),
            ],
            options={
                'verbose_name': 'تنظیمات سایت',
                'verbose_name_plural': 'تنظیمات سایت',
            },
        ),
    ]