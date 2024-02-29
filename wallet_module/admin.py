from django.contrib import admin

from wallet_module.models import Wallet, Transaction, WalletSetting

# Register your models here.

admin.site.register(Wallet)
admin.site.register(WalletSetting)
admin.site.register(Transaction)
