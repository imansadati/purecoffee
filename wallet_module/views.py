from django.contrib import messages
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from decimal import Decimal

from wallet_module.models import Transaction, Wallet, WalletSetting


# Create your views here.

def make_purchase_wallet(request: HttpRequest, total_price, current_order):
    wallet = Wallet.objects.get_or_create(user=request.user)[0]

    wallet_settings = WalletSetting.objects.first()
    percentage_to_add = wallet_settings.percentage_to_add

    bonus_amount = int((percentage_to_add / 100) * total_price)

    wallet.balance += bonus_amount
    wallet.save()

    Transaction.objects.create(user=request.user, amount=bonus_amount, order_id=current_order)
    messages.success(request, 'کیف پول شما با موفقیت شارژ شد')
