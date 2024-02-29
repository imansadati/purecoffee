from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.db.models import Q, F, OuterRef, Subquery
from django.http import HttpRequest, JsonResponse, Http404
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.generic import ListView
from account_module.models import User
from order_module.models import Address
from order_module.models import Order, OrderDetail
from product_module.models import ProductColor, Coupon
from site_module.models import SiteSetting
from user_panel_module.forms import CheckoutForm, ChangePasswordUserForm, CouponForm
from utils.check_accessibility import check_basket_empty
from utils.remove_unavailable_products import remove_unavailable_products_from_basket
from wallet_module.models import Wallet, WalletSetting
from wallet_module.views import make_purchase_wallet
from order_module.views import request_payment
from django.db.models import Q, Sum, Case, When, Value, IntegerField


@login_required
def user_basket(request: HttpRequest):
    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                             user_id=request.user.id)

    remove_unavailable_products_from_basket(current_order)

    sum = current_order.calculate_total_price()
    context = {
        'order': current_order,
        'sum': sum,
    }
    return render(request, 'user_panel_module/user_basket.html', context)


# def basket_count(request):
#     products_count = {}
#
#     if request.user.is_authenticated:
#         # Get the products in the user's basket
#         basket = Order.objects.filter(user=request.user, is_paid=False).first()
#
#         if basket:
#             # Iterate through the items in the basket and count each product
#             for item in basket.orderdetail_set.all():
#                 product_id = item.product.id
#                 count = item.count
#                 products_count[product_id] = count
#
#     return JsonResponse({'products_count': products_count})

@method_decorator(check_basket_empty, name='dispatch')
class CheckoutView(View):

    def get(self, request: HttpRequest):
        current_order = Order.objects.get(is_paid=False, user_id=request.user.id)
        current_wallet, wallet = Wallet.objects.get_or_create(user=request.user)
        wallet_settings: WalletSetting = WalletSetting.objects.first()
        user_address: Address = Address.objects.filter(user_id=request.user.id).first()
        site_setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
        coupon_form = CouponForm()

        payable_amount = current_order.calculate_total_price()

        if current_wallet.balance >= 1:
            if payable_amount >= wallet_settings.min_purchase:
                payable_amount -= current_wallet.balance

        payable_amount += site_setting.shipping_amount

        if user_address:
            initial_data = {
                'full_name': user_address.full_name,
                'phone_number': user_address.phone_number,
                'province': user_address.province,
                'city': user_address.city,
                'exact_address': user_address.exact_address,
                'plaque': user_address.plaque,
                'postal_code': user_address.postal_code,
            }
            checkout_form = CheckoutForm(initial=initial_data)
        else:
            checkout_form = CheckoutForm()

        total_amount = current_order.calculate_total_price()
        min_purchase = wallet_settings.min_purchase / 1000
        context = {
            'order': current_order,
            'sum': total_amount,
            'checkout_form': checkout_form,
            'payable_amount': payable_amount,
            'wallet': current_wallet,
            'min_purchase': min_purchase,
            'coupon_form': coupon_form,
            'site_setting': site_setting
        }
        return render(request, 'user_panel_module/checkout.html', context)

    def post(self, request: HttpRequest):
        checkout_form = CheckoutForm(request.POST)
        coupon_form = CouponForm(request.POST)
        wallet_settings: WalletSetting = WalletSetting.objects.first()
        current_wallet: Wallet = Wallet.objects.filter(user_id=request.user.id).first()
        current_order = Order.objects.get(is_paid=False, user_id=request.user.id)
        site_setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
        total_amount = current_order.calculate_total_price()
        min_purchase = wallet_settings.min_purchase / 1000

        payable_amount = current_order.calculate_total_price()

        if current_wallet.balance >= 1:
            if payable_amount >= wallet_settings.min_purchase:
                payable_amount -= current_wallet.balance

        payable_amount += site_setting.shipping_amount

        user_address: Address = Address.objects.filter(user_id=request.user.id).first()

        if checkout_form.is_valid():
            full_name = checkout_form.cleaned_data.get('full_name')
            phone_number = checkout_form.cleaned_data.get('phone_number')
            province = checkout_form.cleaned_data.get('province')
            city = checkout_form.cleaned_data.get('city')
            exact_address = checkout_form.cleaned_data.get('exact_address')
            plaque = checkout_form.cleaned_data.get('plaque')
            postal_code = checkout_form.cleaned_data.get('postal_code')

            existing_address: Address = Address.objects.filter(phone_number=phone_number, full_name=full_name).first()

            if existing_address:
                existing_address.city = city
                existing_address.province = province
                existing_address.exact_address = exact_address
                existing_address.plaque = plaque
                existing_address.postal_code = postal_code
                existing_address.save()
            else:
                new_address = Address(
                    user_id=request.user.id,
                    full_name=full_name,
                    phone_number=phone_number,
                    province=province,
                    city=city,
                    exact_address=exact_address,
                    plaque=plaque,
                    postal_code=postal_code,
                )
                new_address.save()

            current_order.address = existing_address or new_address
            current_order.save()
            return redirect(reverse('request_payment'))

        if coupon_form.is_valid():
            coupon_code = coupon_form.cleaned_data['coupon']
            try:
                coupon = Coupon.objects.get(code=coupon_code, is_active=True)
                if coupon.valid_from <= timezone.now() <= coupon.valid_to:
                    if request.user not in coupon.used_by.all():
                        # discount_amount = (coupon.discount / 100) * payable_amount
                        discount_amount = (100 - coupon.discount) / 100
                        coupon_name = coupon.title
                        # payable_amount -= discount_amount
                        coupon.used_by.add(request.user)
                        request.session['coupon_data'] = {
                            'discount_amount': discount_amount,
                            'coupon_name': coupon_name
                        }
                        payable_amount *= discount_amount
                        messages.success(request, 'کد تخفیف با موفقیت اعمال شد')
                    else:
                        coupon_form.add_error('coupon', 'شما قبلاً از این کد تخفیف استفاده کرده‌اید')
                else:
                    coupon_form.add_error('coupon', 'کد تخفیف در دسترس نیست')

            except Coupon.DoesNotExist:
                coupon_form.add_error('coupon', 'کد تخفیف اعمال شده وجود ندارد')

        if user_address:
            initial_data = {
                'full_name': user_address.full_name,
                'phone_number': user_address.phone_number,
                'province': user_address.province,
                'city': user_address.city,
                'exact_address': user_address.exact_address,
                'plaque': user_address.plaque,
                'postal_code': user_address.postal_code,
            }
            checkout_form = CheckoutForm(initial=initial_data)
        else:
            checkout_form = CheckoutForm()

        context = {
            'order': current_order,
            'sum': total_amount,
            'checkout_form': checkout_form,
            'min_purchase': min_purchase,
            'payable_amount': int(payable_amount),
            'wallet': current_wallet,
            'coupon_form': coupon_form,
            'site_setting': site_setting
        }
        return render(request, 'user_panel_module/checkout.html', context)


@login_required
def change_order_detail(request: HttpRequest):
    detail_id = request.GET.get('detail_id')
    color = request.GET.get('color')
    state = request.GET.get('state')
    if detail_id is None or state is None:
        return JsonResponse({
            'status': 'not_found_detail_or_state'
        })

    order_detail = OrderDetail.objects.filter(id=detail_id, order__user_id=request.user.id,
                                              order__is_paid=False).first()
    product_color: ProductColor = ProductColor.objects.filter(product_id=order_detail.product.id, is_active=True,
                                                              status=True, title=color).first()

    if detail_id is None:
        return JsonResponse({
            'status': 'detail_not_found'
        })
    if product_color is not None:
        if state == 'increase':
            if product_color.count > order_detail.count:
                order_detail.count += 1
                order_detail.final_price = order_detail.product.price * order_detail.count
                order_detail.save()
            else:
                return JsonResponse({
                    'status': 'product_finished',
                    'text': 'تعداد محصول وارد شده بیشتر از موجودی است',
                    'confirm_button_text': 'باشه ممنونم',
                    'icon': 'warning'
                })
        elif state == 'decrease':
            if order_detail.count == 1:
                order_detail.delete()
            else:
                order_detail.count -= 1
                order_detail.final_price = order_detail.product.price * order_detail.count
                order_detail.save()
        else:
            return JsonResponse({
                'status': 'state_invalid'
            })
    else:
        if state == 'increase':
            if order_detail.product.availability_count > order_detail.count:
                order_detail.count += 1
                order_detail.final_price = order_detail.product.price * order_detail.count
                order_detail.save()
            else:
                return JsonResponse({
                    'status': 'product_finished',
                    'text': 'تعداد محصول وارد شده بیشتر از موجودی است',
                    'confirm_button_text': 'باشه ممنونم',
                    'icon': 'warning'
                })

        elif state == 'decrease':
            if order_detail.count == 1:
                order_detail.delete()
            else:
                order_detail.count -= 1
                order_detail.final_price = order_detail.product.price * order_detail.count
                order_detail.save()
        else:
            return JsonResponse({
                'status': 'state_invalid'
            })

    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                             user_id=request.user.id)
    total_amount = 0
    for order_detail in current_order.orderdetail_set.all():
        total_amount += order_detail.product.price * order_detail.count

    context = {
        'order': current_order,
        'sum': total_amount
    }

    return JsonResponse({
        'status': 'success',
        'body': render_to_string('user_panel_module/user_basket.html', context)
    })


@login_required
def remove_order_detail(request):
    detail_id = request.GET.get('detail_id')

    if detail_id is None:
        return JsonResponse({
            'status': 'detail_not_found'
        })

    deleted_count, deleted_dict = OrderDetail.objects.filter(id=detail_id, order__is_paid=False,
                                                             order__user_id=request.user.id).delete()
    if deleted_count == 0:
        return JsonResponse({
            'status': 'detail_not_found'
        })

    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False,
                                                                                             user_id=request.user.id)
    total_amount = 0
    for order_detail in current_order.orderdetail_set.all():
        total_amount += order_detail.product.price * order_detail.count

    context = {
        'order': current_order,
        'sum': total_amount
    }

    return JsonResponse({
        'status': 'success',
        'body': render_to_string('user_panel_module/user_basket.html', context)
    })


@login_required
def dashboard(request: HttpRequest):
    current_user: User = User.objects.filter(id=request.user.id).first()
    current_address: Address = Address.objects.filter(user_id=request.user.id).first()
    wallet: Wallet = Wallet.objects.filter(user=request.user).first()
    context = {
        'current_user': current_user,
        'current_address': current_address,
        'wallet': wallet
    }
    return render(request, 'user_panel_module/user_dashboard.html', context)


@method_decorator(login_required, name='dispatch')
class ChangePasswordUser(View):
    def get(self, request: HttpRequest):
        change_pass_form = ChangePasswordUserForm()
        context = {
            'form': change_pass_form
        }
        return render(request, 'user_panel_module/user_change_password.html', context)

    def post(self, request: HttpRequest):
        change_pass_form = ChangePasswordUserForm(request.POST)
        if change_pass_form.is_valid():
            user: User = User.objects.filter(id=request.user.id).first()
            new_pass = change_pass_form.cleaned_data.get('new_password')
            current_pass = change_pass_form.cleaned_data.get('current_password')
            if user.check_password(current_pass):
                user.set_password(new_pass)
                user.save()
                logout(request)
                return redirect(reverse('login_page'))
            else:
                change_pass_form.add_error('current_password', 'کلمه عبور وارد شده اشتباه می باشد')

        context = {
            'form': change_pass_form
        }
        return render(request, 'user_panel_module/user_change_password.html', context)


@method_decorator(login_required, name='dispatch')
class UserShopping(ListView):
    model = Order
    template_name = 'user_panel_module/user_shopping_page.html'
    paginate_by = 10

    def get_queryset(self):
        query = super().get_queryset()
        query = query.filter(user_id=self.request.user.id, is_paid=True).order_by('-id')
        return query


@login_required
def user_detail_shopping(request: HttpRequest, order_id):
    order = Order.objects.filter(id=order_id, user_id=request.user.id).first()
    if order is None:
        raise Http404('سبد خرید مورد نظر یافت نشد')
    context = {
        'order': order
    }
    return render(request, 'user_panel_module/user_detail_shopping.html', context)
