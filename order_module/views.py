import datetime
import json

import requests
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, JsonResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from CoffeeShop import settings
from product_module.models import Product, ProductColor
from site_module.models import SiteSetting
from utils.update_product_count import update_product_counts
from wallet_module.models import Wallet, WalletSetting, Transaction
from wallet_module.views import make_purchase_wallet
from .models import Order, OrderDetail

# ? sandbox merchant
if settings.SANDBOX:
    sandbox = "sandbox"
else:
    sandbox = "www"

ZP_API_REQUEST = f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = (
    f"https://{sandbox}.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
)
ZP_API_STARTPAY = f"https://{sandbox}.zarinpal.com/pg/StartPay/"
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید"  # Required
phone = "09192710364"  # Optional
# Important: need to edit for really server.
CallbackURL = "http://127.0.0.1:8000/order/verify-payment/"


def add_product_to_order(request: HttpRequest):
    product_id = int(request.GET.get("id"))
    count = int(request.GET.get("count"))
    color = request.GET.get("color")
    grind = request.GET.get("grind")

    if count < 1:
        return JsonResponse(
            {
                "status": "invalid_count",
                "text": "مقدار وارد شده معتبر نمی باشد",
                "confirm_button_text": "مرسی از شما",
                "icon": "warning",
            }
        )

    if request.user.is_authenticated:
        product = Product.objects.filter(
            id=product_id, is_active=True, status=True
        ).first()
        product_color = ProductColor.objects.filter(
            product_id=product_id, is_active=True, status=True, title=color
        ).first()

        if product:
            if product_color is not None:

                if product_color.count >= count:
                    current_order, created = Order.objects.get_or_create(
                        is_paid=False, user_id=request.user.id
                    )

                    current_order_detail = current_order.orderdetail_set.filter(
                        product_id=product_id, color=color, grind=grind
                    ).first()
                    if current_order_detail is not None:

                        current_order_detail.count += count
                        if product_color.count >= current_order_detail.count:
                            if count == 1:
                                sum = (current_order_detail.count + count) - 1
                                total = product.price * sum
                                current_order_detail.final_price = total
                                current_order_detail.save()
                            else:
                                sum = (current_order_detail.count + count) - 2
                                total = product.price * sum
                                current_order_detail.final_price = total
                                current_order_detail.save()
                        else:
                            return JsonResponse(
                                {
                                    "status": "product_finished",
                                    "text": "تعداد محصول وارد شده بیشتر از موجودی است",
                                    "confirm_button_text": "باشه ممنونم",
                                    "icon": "warning",
                                }
                            )

                    else:
                        new_detail = OrderDetail(
                            order_id=current_order.id,
                            product_id=product_id,
                            count=count,
                            grind=grind,
                            color=color,
                            final_price=product.price * count,
                        )
                        new_detail.save()

                    return JsonResponse(
                        {
                            "status": "success",
                            "text": "محصول مورد نظر با موفقیت به سبد خرید شما اضافه شد",
                            "confirm_button_text": "باشه ممنونم",
                            "icon": "success",
                        }
                    )
                else:
                    return JsonResponse(
                        {
                            "status": "product_finished",
                            "text": "تعداد محصول وارد شده بیشتر از موجودی است",
                            "confirm_button_text": "باشه ممنونم",
                            "icon": "warning",
                        }
                    )
            else:
                if product.availability_count is not None:
                    if product.availability_count >= count:
                        current_order, created = Order.objects.get_or_create(
                            is_paid=False, user_id=request.user.id
                        )

                        current_order_detail = current_order.orderdetail_set.filter(
                            product_id=product_id, color=color, grind=grind
                        ).first()
                        if current_order_detail is not None:
                            current_order_detail.count += count
                            if product.availability_count >= current_order_detail.count:
                                if count == 1:
                                    sum = (current_order_detail.count + count) - 1
                                    total = product.price * sum
                                    current_order_detail.final_price = total
                                    current_order_detail.save()
                                else:
                                    sum = (current_order_detail.count + count) - 2
                                    total = product.price * sum
                                    current_order_detail.final_price = total
                                    current_order_detail.save()
                            else:
                                return JsonResponse(
                                    {
                                        "status": "product_finished",
                                        "text": "تعداد محصول وارد شده بیشتر از موجودی است",
                                        "confirm_button_text": "باشه ممنونم",
                                        "icon": "warning",
                                    }
                                )
                        else:
                            new_detail = OrderDetail(
                                order_id=current_order.id,
                                product_id=product_id,
                                count=count,
                                grind=grind,
                                color=color,
                                final_price=product.price * count,
                            )
                            new_detail.save()

                        return JsonResponse(
                            {
                                "status": "success",
                                "text": "محصول مورد نظر با موفقیت به سبد خرید شما اضافه شد",
                                "confirm_button_text": "باشه ممنونم",
                                "icon": "success",
                            }
                        )
                    else:
                        return JsonResponse(
                            {
                                "status": "product_finished",
                                "text": "تعداد محصول وارد شده بیشتر از موجودی است",
                                "confirm_button_text": "باشه ممنونم",
                                "icon": "warning",
                            }
                        )
                else:
                    return JsonResponse(
                        {
                            "status": "pick_color",
                            "text": "لطفا یک رنگ را انتخاب بکنید",
                            "confirm_button_text": "باشه ممنونم",
                            "icon": "warning",
                        }
                    )
        else:
            return JsonResponse(
                {
                    "status": "not_found",
                    "text": "محصول مورد نظر یافت نشد",
                    "confirm_button_text": "مرسییییی",
                    "icon": "error",
                }
            )
    else:
        return JsonResponse(
            {
                "status": "not_auth",
                "text": "برای افزودن محصول به سبد خرید ابتدا می بایست وارد سایت شوید",
                "confirm_button_text": "ورود به سایت",
                "icon": "error",
            }
        )


@login_required
def request_payment(request: HttpRequest):
    current_order, created = Order.objects.get_or_create(
        is_paid=False, user_id=request.user.id
    )
    current_wallet: Wallet = Wallet.objects.filter(user_id=request.user.id).first()
    wallet_settings: WalletSetting = WalletSetting.objects.first()
    site_setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
    total_price = current_order.calculate_total_price()
    coupon_data = request.session.get(
        "coupon_data"
    )  # Replace with your actual form field name

    # print(coupon_code['code'])

    # del request.session['coupon_data']

    # try:
    #     coupon = Coupon.objects.get(code=coupon_code['code'], is_active=True)
    #     print(coupon)
    #     if coupon.valid_from <= timezone.now() <= coupon.valid_to:
    #         if request.user not in coupon.used_by.all():
    #             discount_amount = (coupon.discount / 100) * total_price
    #             total_price -= discount_amount
    #             # coupon.used_by.add(request.user)
    #             # messages.success(request, 'کد تخفیف با موفقیت اعمال شد.')
    #             del request.session['coupon_data']
    #         else:
    #             messages.error(request, 'شما قبلاً از این کد تخفیف استفاده کرده‌اید.')
    #     else:
    #         messages.error(request, 'کد تخفیف در دسترس نیست.')
    # except Coupon.DoesNotExist:
    #     messages.error(request, 'کد تخفیف اعمال شده وجود ندارد.')

    # 2. Deduct wallet balance if applicable
    if current_wallet.balance >= 1:
        if total_price >= wallet_settings.min_purchase:
            total_price -= current_wallet.balance

    total_price += site_setting.shipping_amount

    if coupon_data:
        discount_amount = coupon_data["discount_amount"]
        total_price *= discount_amount

    # 3. Ensure total_price is non-negative
    total_price = max(total_price, 0)

    if total_price == 0:
        return redirect(reverse("user_basket"))

    # if not total_price == 0:
    #     if current_wallet.balance >= 1:
    #         if total_price >= wallet_settings.min_purchase:
    #             total_price -= current_wallet.balance
    #         else:
    #             return total_price
    #     else:
    #         return total_price
    # else:
    #     return redirect(reverse('user_basket'))
    #
    # if total_price == 0:
    #     return redirect(reverse('user_basket'))
    # else:
    #     total_price

    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": total_price,
        "Description": description,
        "Phone": phone,
        "CallbackURL": CallbackURL,
    }
    data = json.dumps(data)
    headers = {"content-type": "application/json", "content-length": str(len(data))}
    try:
        response = requests.post(
            url=ZP_API_REQUEST, data=data, headers=headers, timeout=10
        )

        if response.status_code == 200:
            response = response.json()
            if response["Status"] == 100:
                # return {'status': True, 'url': ZP_API_STARTPAY + str(response['Authority']),
                #         'authority': response['Authority']}
                url = ZP_API_STARTPAY + str(response["Authority"])
                return HttpResponseRedirect(url)
                # return redirect(ZP_API_STARTPAY.format(authority=response['Authority']))
            else:
                return {"status": False, "code": str(response["Status"])}
        return response

    except requests.exceptions.Timeout:
        return {"status": False, "code": "timeout"}
    except requests.exceptions.ConnectionError:
        return {"status": False, "code": "connection error"}


@login_required
def verify_payment(request: HttpRequest):
    current_order, created = Order.objects.get_or_create(
        is_paid=False, user_id=request.user.id
    )
    current_wallet: Wallet = Wallet.objects.filter(user_id=request.user.id).first()
    wallet_settings: WalletSetting = WalletSetting.objects.first()
    site_setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
    current_orderdetail: OrderDetail = OrderDetail.objects.filter(order=current_order)
    total_price = current_order.calculate_total_price()
    authority = request.GET["Authority"]
    coupon_data = request.session.get(
        "coupon_data"
    )  # Replace with your actual form field name

    # 2. Deduct wallet balance if applicable
    if current_wallet.balance >= 1:
        if total_price >= wallet_settings.min_purchase:
            total_price -= current_wallet.balance

    total_price += site_setting.shipping_amount

    if coupon_data:
        discount_amount = coupon_data["discount_amount"]
        coupon_name = coupon_data["coupon_name"]
        total_price *= discount_amount
        current_order.coupon = coupon_name

        del request.session["coupon_data"]

    data = {
        "MerchantID": settings.MERCHANT,
        "Amount": total_price,
        "Authority": authority,
    }
    data = json.dumps(data)
    # set content length by data
    headers = {"content-type": "application/json", "content-length": str(len(data))}
    response = requests.post(ZP_API_VERIFY, data=data, headers=headers)
    print(response)

    if response.status_code == 200:
        response = response.json()
        if response["Status"] == 100:
            current_order.payment_date = datetime.datetime.now()
            current_order.is_paid = True
            current_order.payable_amount = total_price
            current_order.total_amount = current_order.calculate_total_price()
            update_product_counts(current_order)
            if current_order.is_paid:
                if current_wallet.balance >= 1 and wallet_settings.min_purchase:
                    if total_price > wallet_settings.min_purchase:
                        total_price -= current_wallet.balance
                        current_order.transaction_amount = current_wallet.balance
                        current_wallet.balance = 0
                        current_wallet.save()
                        make_purchase_wallet(request, total_price, current_order.id)
                    else:
                        Transaction.objects.create(
                            user=request.user, amount=0, order_id=current_order.id
                        )
                        current_order.transaction_amount = 0
                else:
                    make_purchase_wallet(request, total_price, current_order.id)
            current_order.save()

            ref_str = response["RefID"]
            return render(
                request,
                "order_module/payment_result.html",
                context={
                    "success": f"تراکنش شما با کد پیگیری {ref_str} با موفقیت انجام شد"
                },
            )
        else:
            return render(
                request,
                "order_module/payment_result.html",
                context={"error": str(response["Status"])},
            )
    return render(
        request, "order_module/payment_result.html", context={"error": str(response)}
    )
