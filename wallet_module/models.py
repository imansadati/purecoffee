from django.db import models

from account_module.models import User
from order_module.models import Order


# Create your models here.


class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='کاربر')
    balance = models.IntegerField(default=0, verbose_name='موجودی کیف پول')

    def save(self, *args, **kwargs):
        if self.balance < 0:
            self.balance = 0
        super(Wallet, self).save()

    def __str__(self):
        return self.user.username


class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='سبد خرید')
    amount = models.IntegerField(default=0, verbose_name='مبلغ تراکنش')
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ انجام تراکنش')

    def __str__(self):
        return self.user.username


class WalletSetting(models.Model):
    percentage_to_add = models.IntegerField(default=5, verbose_name='درصد اضافه شدن به سبد خرید')
    min_purchase = models.BigIntegerField(default=200000, verbose_name='حداقل خرید')
