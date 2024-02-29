from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    otp_create_time = models.DateTimeField(auto_now=True, verbose_name='تاریخ ایجاد کد یکبار مصرف')
    full_name = models.CharField(max_length=120, verbose_name='نام و نام خانوادگی')
    phone_number = models.CharField(max_length=11, unique=True, verbose_name='شماره موبایل')
    otp = models.PositiveIntegerField(blank=True, null=True, verbose_name='کد یکبار مصرف')

    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران'

    def __str__(self):
        if self.first_name and self.last_name is not None:
            return f"{self.first_name} {self.last_name}"
        return self.username
