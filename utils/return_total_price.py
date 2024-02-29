from wallet_module.models import Wallet, WalletSetting
from product_module.models import Coupon
from django.utils import timezone


def calculate_final_total_price(user, current_order, coupon_code=None):
    # Get user's wallet and wallet settings
    current_wallet = Wallet.objects.filter(user=user).first()
    wallet_settings = WalletSetting.objects.first()

    # Calculate the total price of the order
    total_price = current_order.calculate_total_price()

    # Apply coupon logic if a valid coupon code is provided
    if coupon_code:
        try:
            coupon = Coupon.objects.get(code=coupon_code, is_active=True)
            if coupon.valid_from <= timezone.now() <= coupon.valid_to:
                # Calculate the discount amount based on the coupon code
                discount_amount = (coupon.discount / 100) * total_price

                # Reduce the total_price by the discount amount
                total_price -= discount_amount

        except Coupon.DoesNotExist:
            pass  # Coupon code is invalid or not active

    # Check wallet balance and apply it to the total price
    if current_wallet.balance >= 1:
        if total_price >= wallet_settings.min_purchase:
            total_price -= current_wallet.balance

    return total_price
