from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from jalali_date import date2jalali

from account_module.models import User


# Create your models here.


class ContactUs(models.Model):
    title = models.CharField(max_length=300, verbose_name='عنوان')
    email = models.EmailField(max_length=300, verbose_name='ایمیل')
    full_name = models.CharField(max_length=150, verbose_name='نام و نام خانوادگی')
    message = models.TextField(verbose_name='متن پیام')
    create_date = models.DateTimeField(auto_now_add=True, editable=False, verbose_name='تاریخ ایجاد')
    response = models.TextField(null=True, blank=True, verbose_name='متن پاسخ تماس با ما')
    is_read_by_admin = models.BooleanField(default=False, verbose_name='خوانده شده / نشده توسط ادمین')
    is_emailed = models.BooleanField(default=False, verbose_name='پاسخ ایمیل شده / نشده توسط ادمین')

    def get_jalali_create_date(self):
        return date2jalali(self.create_date)

    get_jalali_create_date.short_description = 'تاریخ ایجاد'

    class Meta:
        verbose_name = 'تماس با ما'
        verbose_name_plural = 'لیست تماس با ما'

    def __str__(self):
        return self.title
