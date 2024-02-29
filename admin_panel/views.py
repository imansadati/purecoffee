from builtins import print
from datetime import datetime

import jdatetime
from django.contrib import messages
from django.contrib.auth import login, logout
from django.db.models import Count, Sum, Q
from django.http import HttpRequest
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils import timezone
from django.views import View
from django.views.generic import ListView
from persiantools.jdatetime import JalaliDate

from account_module.models import User
from admin_panel.forms import AdminProductModelForm, AdminCategoryModelForm, AdminTagModelForm, AdminColorModelForm, \
    AdminGrindModelForm, AdminGalleryModelForm, AdminContactModelForm, AdminَArticleModelForm, AdminArticleTagModelForm, \
    AdminArticleCategoryModelForm, AdminSiteSettingModelForm, AdminSiteBannerModelForm, AdminSiteSocialModelForm, \
    AdminSiteTopProductModelForm, AdminSiteCategoryModelForm, AdminSiteFooterBoxModelForm, AdminSiteFooterLinkModelForm, \
    AdminOrderModelForm, AdminWholesaleModelForm, AdminUserModelForm, AddUserAdminForm, LoginUserAdminForm, \
    AdminAddressModelForm, ChangePasswordUserAdminForm, AdminWalletModelForm, AdminTransactionWalletModelForm, \
    AdminWalletSettingModelForm, AdminCouponModelForm
from article_module.models import Article, ArticleTag, ArticleCategory
from contact_module.models import ContactUs
from order_module.models import Order, OrderDetail, Address, Wholesale
from product_module.models import Product, ProductCategory, ProductGrind, ProductTag, ProductColor, ProductGallery, \
    Coupon
from site_module.models import SiteSetting, SiteBanner, SocialMedia, TopProduct, SiteSettingCategory, FooterLinkBox, \
    FooterLink
from wallet_module.models import Wallet, Transaction, WalletSetting


# Create your views here.


def index_admin_panel(request: HttpRequest):
    # show and calculation monthly users added
    all_users = User.objects.filter(is_active=True, is_staff=False, is_superuser=False).count()
    current_month = timezone.now().month
    current_count_user = User.objects.filter(is_active=True, date_joined__month=current_month).count()
    last_month_user = User.objects.filter(is_active=True, date_joined__month=current_month - 1).count()
    if last_month_user != 0:
        percentage_change_users = ((current_count_user - last_month_user) / last_month_user) * 100
    else:
        percentage_change_users = 0

    # show and calculation monthly orders
    current_month = timezone.now().month
    all_orders = Order.objects.filter(is_paid=True).count()
    current_monthly_orders = Order.objects.filter(is_paid=True, payment_date__month=current_month).count()
    previous_monthly_orders = Order.objects.filter(is_paid=True, payment_date__month=current_month - 1).count()
    if previous_monthly_orders != 0:
        percentage_change_orders = ((current_monthly_orders - previous_monthly_orders) / previous_monthly_orders) * 100
    else:
        percentage_change_orders = 0

    # show and calculation monthly sales
    current_month = timezone.now().month
    current_monthly_sales = Order.objects.filter(is_paid=True,
                                                 payment_date__month=current_month).aggregate(
        total_sales=Sum('payable_amount'))
    previous_monthly_sales = Order.objects.filter(is_paid=True,
                                                  payment_date__month=current_month - 1).aggregate(
        total_sales=Sum('payable_amount'))
    current_sales = current_monthly_sales['total_sales'] or 0
    print(current_sales)
    previous_sales = previous_monthly_sales['total_sales'] or 0
    print(f"pre : {previous_sales}")
    if previous_sales != 0:
        percentage_change_sales = ((current_sales - previous_sales) / previous_sales) * 100
    else:
        percentage_change_sales = 0

    # show jalali date
    persian_date = jdatetime.datetime.now().strftime('%d %B %Y')

    # show and calculation daily orders
    current_day = timezone.now().day
    today_orders = Order.objects.filter(is_paid=True, payment_date__day=current_day).count()
    yesterday_orders = Order.objects.filter(is_paid=True, payment_date__day=current_day - 1).count()
    if yesterday_orders != 0:
        percentage_change_orders_yesterday_today = ((today_orders - yesterday_orders) / yesterday_orders) * 100
    else:
        percentage_change_orders_yesterday_today = 0

    # show and calculation daily users
    today_users = User.objects.filter(is_active=True, date_joined__day=current_day).count()
    yesterday_users = User.objects.filter(is_active=True, date_joined__day=current_day - 1).count()
    if yesterday_users != 0:
        percentage_change_users_yesterday_today = ((today_users - yesterday_users) / yesterday_users) * 100
    else:
        percentage_change_users_yesterday_today = 0

    # show and calculation daily messages
    today_messages = ContactUs.objects.filter(create_date__day=current_day).count()
    yesterday_messages = ContactUs.objects.filter(create_date__day=current_day - 1).count()
    if yesterday_messages != 0:
        percentage_change_messages_yesterday_today = ((today_messages - yesterday_messages) / yesterday_messages) * 100
    else:
        percentage_change_messages_yesterday_today = 0

    # top products selling
    top_products = Product.objects.filter(orderdetail__order__is_paid=True).annotate(
        order_count=Count('orderdetail')).order_by('-order_count')[:4]

    # top articles viewed
    top_articles = Article.objects.filter(visit_count__gt=0).order_by('-visit_count')[:4]

    # top province in addresses
    top_provinces = Address.objects.values('province').annotate(count=Count('province')).order_by('-count')[:5]

    # users with high purchases
    top_users = User.objects.filter(order__is_paid=True).annotate(count=Count('order')).order_by('-count')[:5]

    # show latest orders
    latest_orders = Order.objects.filter(is_paid=True).exclude(status='ارسال شده').order_by('-id')[:20]

    context = {
        'all_users': all_users,
        'percentage_change_users': percentage_change_users,
        'percentage_change_orders': percentage_change_orders,
        'all_orders': all_orders,
        'monthly_sales': current_monthly_sales,
        'percentage_change_sales': percentage_change_sales,
        'persian_date': persian_date,
        'today_orders': today_orders,
        'orders_yesterday_today': percentage_change_orders_yesterday_today,
        'percentage_change_users_yesterday_today': percentage_change_users_yesterday_today,
        'today_users': today_users,
        'today_messages': today_messages,
        'percentage_change_messages_yesterday_today': percentage_change_messages_yesterday_today,
        'top_products': top_products,
        'top_articles': top_articles,
        'top_provinces': top_provinces,
        'users_high_purchases': top_users,
        'latest_orders': latest_orders,
    }
    return render(request, 'admin_panel/home/index.html', context)


def top_selling_product(request: HttpRequest):
    top_products = Product.objects.filter(orderdetail__order__is_paid=True).annotate(
        order_count=Count('orderdetail')).order_by('-order_count')[:15]
    context = {
        'top_selling_products': top_products,
    }
    return render(request, 'admin_panel/products/top_selling_products.html', context)


def most_view_articles(request: HttpRequest):
    top_articles = Article.objects.filter(visit_count__gt=0).order_by('-visit_count')[:15]
    context = {
        'top_viewed_articles': top_articles
    }
    return render(request, 'admin_panel/articles/most_view_articles.html', context)


def site_nav_component(request: HttpRequest):
    current_user = User.objects.filter(id=request.user.id).first()
    context = {
        'current_user': current_user
    }
    return render(request, 'admin_panel/shared/site_nav_component.html', context)


def site_sidebar_component(request: HttpRequest):
    contact_us_count = ContactUs.objects.filter(is_read_by_admin=False).count()
    order_count = Order.objects.filter(is_paid=True, status='انتظار').count()
    wholesale_count = Wholesale.objects.filter(payment_status=True, status='انتظار').count()
    context = {
        'contact_count': contact_us_count,
        'order_count': order_count,
        'wholesale_count': wholesale_count
    }
    return render(request, 'admin_panel/shared/site_sidebar_component.html', context)


class AdminProductList(ListView):
    model = Product
    template_name = 'admin_panel/products/product_list_view.html'
    paginate_by = 15

    def get_queryset(self):
        query = super().get_queryset()
        query = query.all()
        search_name = self.request.GET.get('search')
        lookup = Q(
            title__icontains=search_name) | Q(description__icontains=search_name) | Q(tag__title__icontains=search_name)
        if search_name:
            products = Product.objects.filter(lookup).distinct()
            return products
        else:
            return query


class EditeAdminProduct(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        productId = kwargs.get('pk')
        current_product = get_object_or_404(Product, id=productId)
        product_form = AdminProductModelForm(instance=current_product)

        context = {
            'form': product_form,
            'current_product': current_product,
        }
        return render(request, 'admin_panel/products/edit_product_admin.html', context)

    def post(self, request: HttpRequest, *args, **kwargs):
        productId = kwargs.get('pk')
        current_product = get_object_or_404(Product, id=productId)
        product_form = AdminProductModelForm(request.POST, request.FILES, instance=current_product)
        if product_form.is_valid():
            product_form.save(commit=True)
            messages.info(request, 'تغییرات با موفقیت ثبت شد')
            return redirect(reverse('product_list_admin_page'))
        else:
            messages.error(request, 'مشکلی در ثبت تغییرات به وجود آمده است')

        context = {
            'form': product_form,
            'current_product': current_product,
        }
        return render(request, 'admin_panel/products/edit_product_admin.html', context)


class AddProductAdmin(View):
    def get(self, request: HttpRequest):
        add_product_form = AdminProductModelForm()
        context = {
            'form': add_product_form
        }
        return render(request, 'admin_panel/products/add_product_admin.html', context)

    def post(self, request: HttpRequest):
        add_product_form = AdminProductModelForm(request.POST, request.FILES)
        if add_product_form.is_valid():
            add_product_form.save()
            messages.info(request, 'محصول با موفقیت ایجاد شد')
            return redirect(reverse('product_list_admin_page'))
        else:
            messages.error(request, 'مشکلی در ایجاد محصول به وجود آمده است')
        context = {
            'form': add_product_form
        }
        return render(request, 'admin_panel/products/add_product_admin.html', context)


class AdminProductCategoryList(ListView):
    model = ProductCategory
    template_name = 'admin_panel/products/category/category_list_view.html'
    paginate_by = 15

    def get_queryset(self):
        query = super().get_queryset()
        query = query.all()
        search_name = self.request.GET.get('search')
        lookup = Q(
            title__icontains=search_name) | Q(url_title__icontains=search_name)
        if search_name:
            products = ProductCategory.objects.filter(lookup).distinct()
            return products
        else:
            return query


class AddProductCategory(View):
    def get(self, request: HttpRequest):
        add_category_form = AdminCategoryModelForm()
        context = {
            'form': add_category_form
        }
        return render(request, 'admin_panel/products/category/add_category_admin.html', context)

    def post(self, request: HttpRequest):
        add_category_form = AdminCategoryModelForm(request.POST)
        if add_category_form.is_valid():
            add_category_form.save()
            messages.info(request, 'دسته بندی با موفقیت ایجاد شد')
            return redirect(reverse('product_category_list_admin_page'))
        else:
            messages.error(request, 'مشکلی در ایجاد دسته بندی به وجود آمده است')
        context = {
            'form': add_category_form
        }
        return render(request, 'admin_panel/products/category/add_category_admin.html', context)


class EditeAdminProductCategory(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        categoryId = kwargs.get('pk')
        current_category = get_object_or_404(ProductCategory, id=categoryId)
        edit_category_form = AdminCategoryModelForm(instance=current_category)
        context = {
            'form': edit_category_form,
            'current_category': current_category
        }
        return render(request, 'admin_panel/products/category/edit_category_admin.html', context)

    def post(self, request: HttpRequest, *args, **kwargs):
        categoryId = kwargs.get('pk')
        current_category = get_object_or_404(ProductCategory, id=categoryId)
        edit_category_form = AdminCategoryModelForm(request.POST, instance=current_category)
        if edit_category_form.is_valid():
            edit_category_form.save()
            messages.info(request, 'تغییرات با موفقیت ثبت شد')
            return redirect(reverse('product_category_list_admin_page'))
        else:
            messages.error(request, 'مشکلی در تغییر دسته بندی به وجود آمده است')
        context = {
            'form': edit_category_form,
            'current_category': current_category
        }
        return render(request, 'admin_panel/products/category/edit_category_admin.html', context)


class AdminProductTagList(ListView):
    model = ProductTag
    template_name = 'admin_panel/products/tag/tag_list_view_admin.html'
    paginate_by = 15

    def get_queryset(self):
        query = super().get_queryset()
        search_name = self.request.GET.get('search')
        lookup = Q(
            title__icontains=search_name) | Q(url_title__icontains=search_name)
        if search_name:
            products = ProductTag.objects.filter(lookup).distinct()
            return products
        else:
            return query


class AddProductTag(View):
    def get(self, request: HttpRequest):
        add_tag_form = AdminTagModelForm()
        context = {
            'form': add_tag_form
        }
        return render(request, 'admin_panel/products/tag/add_tag_admin.html', context)

    def post(self, request: HttpRequest):
        add_tag_form = AdminTagModelForm(request.POST)
        if add_tag_form.is_valid():
            add_tag_form.save()
            messages.info(request, 'تگ با موفقیت ایجاد شد')
            return redirect(reverse('product_tag_list_admin_page'))
        else:
            messages.error(request, 'مشکلی در ایجاد تگ به وجود آمده است')
        context = {
            'form': add_tag_form
        }
        return render(request, 'admin_panel/products/tag/add_tag_admin.html', context)


class EditeAdminProductTag(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        tagId = kwargs.get('pk')
        current_tag = get_object_or_404(ProductTag, id=tagId)
        edit_tag_form = AdminTagModelForm(instance=current_tag)
        context = {
            'form': edit_tag_form,
            'current_tag': current_tag
        }
        return render(request, 'admin_panel/products/tag/edit_tag_admin.html', context)

    def post(self, request: HttpRequest, *args, **kwargs):
        tagId = kwargs.get('pk')
        current_tag = get_object_or_404(ProductTag, id=tagId)
        edit_tag_form = AdminTagModelForm(request.POST, instance=current_tag)
        if edit_tag_form.is_valid():
            edit_tag_form.save()
            messages.info(request, 'تغییرات با موفقیت ثبت شد')
            return redirect(reverse('product_tag_list_admin_page'))
        else:
            messages.error(request, 'مشکلی در تغییر تگ به وجود آمده است')
        context = {
            'form': edit_tag_form,
            'current_tag': current_tag
        }
        return render(request, 'admin_panel/products/tag/edit_tag_admin.html', context)


class AdminProductColorList(ListView):
    model = ProductColor
    template_name = 'admin_panel/products/color/color_list_view_admin.html'
    paginate_by = 15

    def get_queryset(self):
        query = super().get_queryset()
        query = query.all()
        search_name = self.request.GET.get('search')
        lookup = Q(
            title__icontains=search_name) | Q(product__title__icontains=search_name)
        if search_name:
            products = ProductColor.objects.filter(lookup).distinct()
            return products
        else:
            return query


class AddProductColor(View):
    def get(self, request: HttpRequest):
        add_color_form = AdminColorModelForm()
        context = {
            'form': add_color_form
        }
        return render(request, 'admin_panel/products/color/add_color_admin.html', context)

    def post(self, request: HttpRequest):
        add_color_form = AdminColorModelForm(request.POST)
        if add_color_form.is_valid():
            add_color_form.save()
            messages.info(request, 'رنگ با موفقیت ایجاد شد')
            return redirect(reverse('product_color_list_admin_page'))
        else:
            messages.error(request, 'مشکلی در ایجاد رنگ به وجود آمده است')
        context = {
            'form': add_color_form
        }
        return render(request, 'admin_panel/products/color/add_color_admin.html', context)


class EditeAdminProductColor(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        colorId = kwargs.get('pk')
        current_color = get_object_or_404(ProductColor, id=colorId)
        edit_color_form = AdminColorModelForm(instance=current_color)
        context = {
            'form': edit_color_form,
            'current_color': current_color
        }
        return render(request, 'admin_panel/products/color/edit_color_admin.html', context)

    def post(self, request: HttpRequest, *args, **kwargs):
        colorId = kwargs.get('pk')
        current_color = get_object_or_404(ProductColor, id=colorId)
        edit_color_form = AdminColorModelForm(request.POST, request.FILES, instance=current_color)
        if edit_color_form.is_valid():
            edit_color_form.save()
            messages.info(request, 'تغییرات با موفقیت ثبت شد')
            return redirect(reverse('product_color_list_admin_page'))
        else:
            messages.error(request, 'مشکلی در تغییر رنگ به وجود آمده است')
        context = {
            'form': edit_color_form,
            'current_color': current_color
        }
        return render(request, 'admin_panel/products/color/edit_color_admin.html', context)


class AdminProductGrindList(ListView):
    model = ProductGrind
    template_name = 'admin_panel/products/grind/grind_list_view_admin.html'
    paginate_by = 15

    def get_queryset(self):
        query = super().get_queryset()
        query = query.all()
        search_name = self.request.GET.get('search')
        lookup = Q(title__icontains=search_name)
        if search_name:
            products = ProductGrind.objects.filter(lookup).distinct()
            return products
        else:
            return query


class AddProductGrind(View):
    def get(self, request: HttpRequest):
        add_grind_form = AdminGrindModelForm()
        context = {
            'form': add_grind_form
        }
        return render(request, 'admin_panel/products/grind/add_grind_admin.html', context)

    def post(self, request: HttpRequest):
        add_grind_form = AdminGrindModelForm(request.POST)
        if add_grind_form.is_valid():
            add_grind_form.save()
            messages.info(request, 'آسیاب با موفقیت ایجاد شد')
            return redirect(reverse('product_grind_list_admin_page'))
        else:
            messages.error(request, 'مشکلی در ایجاد آسیاب به وجود آمده است')
        context = {
            'form': add_grind_form
        }
        return render(request, 'admin_panel/products/grind/add_grind_admin.html', context)


class EditeAdminProductGrind(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        grindId = kwargs.get('pk')
        current_grind = get_object_or_404(ProductGrind, id=grindId)
        edit_grind_form = AdminGrindModelForm(instance=current_grind)
        context = {
            'form': edit_grind_form,
            'current_grind': current_grind
        }
        return render(request, 'admin_panel/products/grind/edit_grind_admin.html', context)

    def post(self, request: HttpRequest, *args, **kwargs):
        grindId = kwargs.get('pk')
        current_grind = get_object_or_404(ProductGrind, id=grindId)
        edit_grind_form = AdminTagModelForm(request.POST, instance=current_grind)
        if edit_grind_form.is_valid():
            edit_grind_form.save()
            messages.info(request, 'تغییرات با موفقیت ثبت شد')
            return redirect(reverse('product_grind_list_admin_page'))
        else:
            messages.error(request, 'مشکلی در تغییر آسیاب به وجود آمده است')
        context = {
            'form': edit_grind_form,
            'current_grind': current_grind
        }
        return render(request, 'admin_panel/products/grind/edit_grind_admin.html', context)


class AdminProductGalleryList(ListView):
    model = ProductGallery
    template_name = 'admin_panel/products/gallery/gallery_list_view_admin.html'
    paginate_by = 15

    def get_queryset(self):
        query = super().get_queryset()
        query = query.all()
        search_name = self.request.GET.get('search')
        lookup = Q(product__title__icontains=search_name)
        if search_name:
            products = ProductGallery.objects.filter(lookup).distinct()
            return products
        else:
            return query


class AddProductGallery(View):
    def get(self, request: HttpRequest):
        add_gallery_form = AdminGalleryModelForm()
        context = {
            'form': add_gallery_form
        }
        return render(request, 'admin_panel/products/gallery/add_gallery_admin.html', context)

    def post(self, request: HttpRequest):
        add_gallery_form = AdminGalleryModelForm(request.POST, request.FILES)
        if add_gallery_form.is_valid():
            add_gallery_form.save()
            messages.info(request, 'تصویر با موفقیت ایجاد شد')
            return redirect(reverse('product_gallery_list_admin_page'))
        else:
            messages.error(request, 'مشکلی در ایجاد تصویر به وجود آمده است')
        context = {
            'form': add_gallery_form
        }
        return render(request, 'admin_panel/products/gallery/add_gallery_admin.html', context)


class EditeAdminProductGallery(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        galleryId = kwargs.get('pk')
        current_gallery = get_object_or_404(ProductGallery, id=galleryId)
        edit_gallery_form = AdminGalleryModelForm(instance=current_gallery)
        context = {
            'form': edit_gallery_form,
            'current_gallery': current_gallery
        }
        return render(request, 'admin_panel/products/gallery/edit_gallery_admin.html', context)

    def post(self, request: HttpRequest, *args, **kwargs):
        galleryId = kwargs.get('pk')
        current_gallery = get_object_or_404(ProductGallery, id=galleryId)
        edit_gallery_form = AdminGalleryModelForm(request.POST, request.FILES, instance=current_gallery)
        if edit_gallery_form.is_valid():
            edit_gallery_form.save()
            messages.info(request, 'تغییرات با موفقیت ثبت شد')
            return redirect(reverse('product_gallery_list_admin_page'))
        else:
            messages.error(request, 'مشکلی در تغییر تصویر به وجود آمده است')
        context = {
            'form': edit_gallery_form,
            'current_gallery': current_gallery
        }
        return render(request, 'admin_panel/products/gallery/edit_gallery_admin.html', context)


def delete_tag(request: HttpRequest, pk):
    product_tag = get_object_or_404(ProductTag, pk=pk)

    if request.method == 'POST':
        product_tag.delete()
        messages.info(request, 'تغییرات با موفقیت ثبت شد')
        return redirect(reverse('product_tag_list_admin_page'))
    return redirect(reverse('edit_product_tag_admin_page'))


def delete_product(request: HttpRequest, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'POST':
        product.delete()
        messages.info(request, 'تغییرات با موفقیت ثبت شد')
        return redirect(reverse('product_list_admin_page'))
    return redirect(reverse('edit_product_admin_page'))


def delete_color(request: HttpRequest, pk):
    product_color = get_object_or_404(ProductColor, pk=pk)

    if request.method == 'POST':
        product_color.delete()
        messages.info(request, 'تغییرات با موفقیت ثبت شد')
        return redirect(reverse('product_color_list_admin_page'))
    return redirect(reverse('edit_product_color_admin_page'))


def delete_gallery(request: HttpRequest, pk):
    product_gallery = get_object_or_404(ProductGallery, pk=pk)

    if request.method == 'POST':
        product_gallery.delete()
        messages.info(request, 'تغییرات با موفقیت ثبت شد')
        return redirect(reverse('product_gallery_list_admin_page'))
    return redirect(reverse('edit_product_gallery_admin_page'))


def delete_category(request: HttpRequest, pk):
    product_category = get_object_or_404(ProductCategory, pk=pk)

    if request.method == 'POST':
        product_category.delete()
        messages.info(request, 'تغییرات با موفقیت ثبت شد')
        return redirect(reverse('product_category_list_admin_page'))
    return redirect(reverse('edit_product_category_admin_page'))


def delete_grind(request: HttpRequest, pk):
    product_grind = get_object_or_404(ProductGrind, pk=pk)

    if request.method == 'POST':
        product_grind.delete()
        messages.info(request, 'تغییرات با موفقیت ثبت شد')
        return redirect(reverse('product_grind_list_admin_page'))
    return redirect(reverse('edit_product_grind_admin_page'))


class AdminContactUsList(ListView):
    model = ContactUs
    template_name = 'admin_panel/contact/contact_list_admin_panel.html'
    paginate_by = 15

    def get_queryset(self):
        query = super().get_queryset()
        query = query.all().order_by('is_read_by_admin')
        search_name = self.request.GET.get('search')
        lookup = Q(full_name__icontains=search_name) | Q(email__icontains=search_name) | Q(title__icontains=search_name)
        if search_name:
            contacts = ContactUs.objects.filter(lookup).distinct()
            return contacts
        return query


class AdminContactUsDetail(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        contactId = kwargs.get('pk')
        current_contact = get_object_or_404(ContactUs, pk=contactId)
        contact_form = AdminContactModelForm(instance=current_contact)

        context = {
            'form': contact_form,
            'contact': current_contact
        }
        return render(request, 'admin_panel/contact/contact_detail_admin_panel.html', context)

    def post(self, request: HttpRequest, *args, **kwargs):
        contactId = kwargs.get('pk')
        current_contact = get_object_or_404(ContactUs, pk=contactId)
        contact_form = AdminContactModelForm(request.POST, instance=current_contact)
        if contact_form.is_valid():
            contact_form.save()
            messages.info(request, 'تغییرات با موفقیت ثبت شد')
            return redirect(reverse('contact_list_admin_page'))
        else:
            messages.error(request, 'مشکلی به وجود آمده است')
        context = {
            'form': contact_form,
            'contact': current_contact
        }
        return render(request, 'admin_panel/contact/contact_detail_admin_panel.html', context)


def delete_contact(request: HttpRequest, pk):
    contact = get_object_or_404(ContactUs, pk=pk)

    if request.method == 'POST':
        contact.delete()
        messages.info(request, 'تغییرات با موفقیت ثبت شد')
        return redirect(reverse('contact_list_admin_page'))
    return redirect(reverse('contact_detail_admin_page'))


class AdminArticleList(ListView):
    model = Article
    template_name = 'admin_panel/articles/articles_list_view.html'
    paginate_by = 15

    def get_queryset(self):
        query = super().get_queryset()
        query = query.all()
        search_name = self.request.GET.get('search')
        lookup = Q(slug__icontains=search_name) | Q(short_description__icontains=search_name) | Q(
            title__icontains=search_name)
        if search_name:
            articles = Article.objects.filter(lookup).distinct()
            return articles
        return query


class AddArticleAdmin(View):
    def get(self, request, *args, **kwargs):
        article_form = AdminَArticleModelForm()
        context = {
            'form': article_form
        }
        return render(request, 'admin_panel/articles/add_article_admin.html', context)

    def post(self, request, *args, **kwargs):
        article_form = AdminَArticleModelForm(request.POST, request.FILES)
        if article_form.is_valid():
            article_form.save()
            messages.info(request, 'مقاله با موفقیت ایجاد شد')
            return redirect(reverse('article_list_admin_page'))
        else:
            messages.error(request, 'مشکلی در ایجاد مقاله به وجود آمده است')
        context = {
            'form': article_form
        }
        return render(request, 'admin_panel/articles/add_article_admin.html', context)


class EditArticleAdmin(View):
    def get(self, request, *args, **kwargs):
        articleId = kwargs.get('pk')
        current_article = get_object_or_404(Article, pk=articleId)
        article_form = AdminَArticleModelForm(instance=current_article)
        context = {
            'form': article_form,
            'current_article': current_article
        }
        return render(request, 'admin_panel/articles/edit_article_admin.html', context)

    def post(self, request, *args, **kwargs):
        articleId = kwargs.get('pk')
        current_article = get_object_or_404(Article, pk=articleId)
        article_form = AdminَArticleModelForm(request.POST, request.FILES, instance=current_article)
        if article_form.is_valid():
            article_form.save()
            messages.info(request, 'تغییرات با موفقیت ثبت شد')
            return redirect(reverse('article_list_admin_page'))
        else:
            messages.error(request, 'مشکلی در ثبت تغییرات به وجود آمده است')

        context = {
            'form': article_form,
            'current_article': current_article
        }
        return render(request, 'admin_panel/articles/edit_article_admin.html', context)


def delete_article(request: HttpRequest, pk):
    article = get_object_or_404(Article, pk=pk)

    if request.method == 'POST':
        article.delete()
        messages.info(request, 'تغییرات با موفقیت ثبت شد')
        return redirect(reverse('article_list_admin_page'))
    return redirect(reverse('edit_article_admin_page'))


class AdminArticleTagList(ListView):
    model = ArticleTag
    template_name = 'admin_panel/articles/tag/article_tag_list_admin.html'
    paginate_by = 15

    def get_queryset(self):
        query = super().get_queryset()
        search_name = self.request.GET.get('search')
        lookup = Q(
            title__icontains=search_name) | Q(url_title__icontains=search_name)
        if search_name:
            article_tags = ArticleTag.objects.filter(lookup).distinct()
            return article_tags
        else:
            return query.order_by('-id')


class AddArticleTagAdmin(View):
    def get(self, request: HttpRequest):
        add_tag_form = AdminArticleTagModelForm()
        context = {
            'form': add_tag_form
        }
        return render(request, 'admin_panel/articles/tag/add_article_tag_admin.html', context)

    def post(self, request: HttpRequest):
        add_tag_form = AdminArticleTagModelForm(request.POST)
        if add_tag_form.is_valid():
            add_tag_form.save()
            messages.info(request, 'تگ با موفقیت ایجاد شد')
            return redirect(reverse('article_tag_list_admin_page'))
        else:
            messages.error(request, 'مشکلی در ایجاد تگ به وجود آمده است')
        context = {
            'form': add_tag_form
        }
        return render(request, 'admin_panel/articles/tag/add_article_tag_admin.html', context)


class EditAdminArticleTag(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        tagId = kwargs.get('pk')
        current_tag = get_object_or_404(ArticleTag, id=tagId)
        edit_tag_form = AdminArticleTagModelForm(instance=current_tag)
        context = {
            'form': edit_tag_form,
            'current_tag': current_tag
        }
        return render(request, 'admin_panel/articles/tag/edit_article_tag_admin.html', context)

    def post(self, request: HttpRequest, *args, **kwargs):
        tagId = kwargs.get('pk')
        current_tag = get_object_or_404(ArticleTag, id=tagId)
        edit_tag_form = AdminArticleTagModelForm(request.POST, instance=current_tag)
        if edit_tag_form.is_valid():
            edit_tag_form.save()
            messages.info(request, 'تغییرات با موفقیت ثبت شد')
            return redirect(reverse('article_tag_list_admin_page'))
        else:
            messages.error(request, 'مشکلی در تغییر تگ به وجود آمده است')
        context = {
            'form': edit_tag_form,
            'current_tag': current_tag
        }
        return render(request, 'admin_panel/articles/tag/edit_article_tag_admin.html', context)


def delete_article_tag(request: HttpRequest, pk):
    article_tag = get_object_or_404(ArticleTag, pk=pk)

    if request.method == 'POST':
        article_tag.delete()
        messages.info(request, 'تغییرات با موفقیت ثبت شد')
        return redirect(reverse('article_tag_list_admin_page'))
    return redirect(reverse('edit_article_tag_admin_page'))


class AdminArticleCategoryList(ListView):
    model = ArticleCategory
    template_name = 'admin_panel/articles/category/article_category_list_admin.html'
    paginate_by = 15

    def get_queryset(self):
        query = super().get_queryset()
        search_name = self.request.GET.get('search')
        lookup = Q(
            title__icontains=search_name) | Q(url_title__icontains=search_name)
        if search_name:
            article_categories = ArticleCategory.objects.filter(lookup).distinct()
            return article_categories
        else:
            return query.order_by('-id')


class AddArticleCategoryAdmin(View):
    def get(self, request: HttpRequest):
        add_category_form = AdminArticleCategoryModelForm()
        context = {
            'form': add_category_form
        }
        return render(request, 'admin_panel/articles/category/add_article_category_admin.html', context)

    def post(self, request: HttpRequest):
        add_category_form = AdminArticleCategoryModelForm(request.POST)
        if add_category_form.is_valid():
            add_category_form.save()
            messages.info(request, 'دسته بندی با موفقیت ایجاد شد')
            return redirect(reverse('article_category_list_admin_page'))
        else:
            messages.error(request, 'مشکلی در ایجاد دسته بندی به وجود آمده است')
        context = {
            'form': add_category_form
        }
        return render(request, 'admin_panel/articles/category/add_article_category_admin.html', context)


class EditAdminArticleCategory(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        catId = kwargs.get('pk')
        current_category = get_object_or_404(ArticleCategory, id=catId)
        edit_category_form = AdminArticleCategoryModelForm(instance=current_category)
        context = {
            'form': edit_category_form,
            'current_category': current_category
        }
        return render(request, 'admin_panel/articles/category/edit_article_category_admin.html', context)

    def post(self, request: HttpRequest, *args, **kwargs):
        catId = kwargs.get('pk')
        current_category = get_object_or_404(ArticleCategory, id=catId)
        edit_category_form = AdminArticleCategoryModelForm(request.POST, instance=current_category)
        if edit_category_form.is_valid():
            edit_category_form.save()
            messages.info(request, 'تغییرات با موفقیت ثبت شد')
            return redirect(reverse('article_category_list_admin_page'))
        else:
            messages.error(request, 'مشکلی در تغییر دسته بندی به وجود آمده است')
        context = {
            'form': edit_category_form,
            'current_category': current_category
        }
        return render(request, 'admin_panel/articles/category/edit_article_category_admin.html', context)


def delete_article_category(request: HttpRequest, pk):
    article_category = get_object_or_404(ArticleCategory, pk=pk)

    if request.method == 'POST':
        article_category.delete()
        messages.info(request, 'تغییرات با موفقیت ثبت شد')
        return redirect(reverse('article_category_list_admin_page'))
    return redirect(reverse('edit_article_category_admin_page'))


class SiteSettingAdminList(ListView):
    model = SiteSetting
    template_name = 'admin_panel/site_setting/site_setting_list_admin.html'
    paginate_by = 10

    def get_queryset(self):
        query = super().get_queryset()
        search_name = self.request.GET.get('search')
        lookup = Q(
            title__icontains=search_name) | Q(url_title__icontains=search_name)
        if search_name:
            site_settings = SiteSetting.objects.filter(lookup).distinct()
            return site_settings
        else:
            return query.order_by('-id')


class AddSiteSettingAdmin(View):
    def get(self, request: HttpRequest):
        add_setting_form = AdminSiteSettingModelForm()
        context = {
            'form': add_setting_form
        }
        return render(request, 'admin_panel/site_setting/add_site_setting_admin.html', context)

    def post(self, request: HttpRequest):
        add_setting_form = AdminSiteSettingModelForm(request.POST, request.FILES)
        if add_setting_form.is_valid():
            add_setting_form.save()
            messages.info(request, 'تنظیمات با موفقیت ایجاد شد')
            return redirect(reverse('site_setting_list_admin_page'))
        else:
            messages.error(request, 'مشکلی در ایجاد تنظیمات جدید به وجود آمده است')
        context = {
            'form': add_setting_form
        }
        return render(request, 'admin_panel/site_setting/add_site_setting_admin.html', context)


class EditAdminSiteSetting(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        settingId = kwargs.get('pk')
        current_setting = get_object_or_404(SiteSetting, id=settingId)
        edit_setting_form = AdminSiteSettingModelForm(instance=current_setting)
        context = {
            'form': edit_setting_form,
            'current_setting': current_setting
        }
        return render(request, 'admin_panel/site_setting/edit_site_setting_admin.html', context)

    def post(self, request: HttpRequest, *args, **kwargs):
        settingId = kwargs.get('pk')
        current_setting = get_object_or_404(SiteSetting, id=settingId)
        edit_setting_form = AdminSiteSettingModelForm(request.POST, request.FILES, instance=current_setting)
        if edit_setting_form.is_valid():
            edit_setting_form.save()
            messages.info(request, 'تغییرات با موفقیت ثبت شد')
            return redirect(reverse('site_setting_list_admin_page'))
        else:
            messages.error(request, 'مشکلی در تغییر تنظیمات به وجود آمده است')
        context = {
            'form': edit_setting_form,
            'current_setting': current_setting
        }
        return render(request, 'admin_panel/site_setting/edit_site_setting_admin.html', context)


def delete_site_setting(request: HttpRequest, pk):
    site_setting = get_object_or_404(SiteSetting, pk=pk)

    if request.method == 'POST':
        site_setting.delete()
        messages.info(request, 'تغییرات با موفقیت ثبت شد')
        return redirect(reverse('site_setting_list_admin_page'))
    return redirect(reverse('edit_site_setting_admin_page'))


class SiteBannerAdminList(ListView):
    model = SiteBanner
    template_name = 'admin_panel/site_setting/banner/site_banner_list_admin.html'
    paginate_by = 10

    def get_queryset(self):
        query = super().get_queryset()
        search_name = self.request.GET.get('search')
        lookup = Q(
            title__icontains=search_name) | Q(url__icontains=search_name) | Q(posision__icontains=search_name)
        if search_name:
            site_banners = SiteBanner.objects.filter(lookup).distinct()
            return site_banners
        else:
            return query.order_by('-id')


class AddSiteBannerAdmin(View):
    def get(self, request: HttpRequest):
        add_banner_form = AdminSiteBannerModelForm()
        context = {
            'form': add_banner_form
        }
        return render(request, 'admin_panel/site_setting/banner/add_site_banner_admin.html', context)

    def post(self, request: HttpRequest):
        add_banner_form = AdminSiteBannerModelForm(request.POST, request.FILES)
        if add_banner_form.is_valid():
            add_banner_form.save()
            messages.info(request, 'بنر با موفقیت ایجاد شد')
            return redirect(reverse('site_banner_list_admin_page'))
        else:
            messages.error(request, 'مشکلی در ایجاد بنر جدید به وجود آمده است')
        context = {
            'form': add_banner_form
        }
        return render(request, 'admin_panel/site_setting/banner/add_site_banner_admin.html', context)


class EditAdminSiteBanner(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        bannerId = kwargs.get('pk')
        current_banner = get_object_or_404(SiteBanner, id=bannerId)
        edit_banner_form = AdminSiteBannerModelForm(instance=current_banner)
        context = {
            'form': edit_banner_form,
            'current_banner': current_banner
        }
        return render(request, 'admin_panel/site_setting/banner/edit_site_banner_admin.html', context)

    def post(self, request: HttpRequest, *args, **kwargs):
        bannerId = kwargs.get('pk')
        current_banner = get_object_or_404(SiteBanner, id=bannerId)
        edit_banner_form = AdminSiteBannerModelForm(request.POST, request.FILES, instance=current_banner)
        if edit_banner_form.is_valid():
            edit_banner_form.save()
            messages.info(request, 'تغییرات با موفقیت ثبت شد')
            return redirect(reverse('site_banner_list_admin_page'))
        else:
            messages.error(request, 'مشکلی در تغییر تنظیمات بنر به وجود آمده است')
        context = {
            'form': edit_banner_form,
            'current_banner': current_banner
        }
        return render(request, 'admin_panel/site_setting/banner/edit_site_banner_admin.html', context)


def delete_site_banner(request: HttpRequest, pk):
    site_banner = get_object_or_404(SiteBanner, pk=pk)

    if request.method == 'POST':
        site_banner.delete()
        messages.info(request, 'تغییرات با موفقیت ثبت شد')
        return redirect(reverse('site_banner_list_admin_page'))
    return redirect(reverse('edit_site_banner_admin_page'))


class SiteSocialAdminList(ListView):
    model = SocialMedia
    template_name = 'admin_panel/site_setting/social_media/site_social_list_admin.html'
    paginate_by = 10

    def get_queryset(self):
        query = super().get_queryset()
        search_name = self.request.GET.get('search')
        lookup = Q(
            instagram__icontains=search_name)
        if search_name:
            site_socials = SocialMedia.objects.filter(lookup).distinct()
            return site_socials
        else:
            return query.order_by('-id')


class AddSiteSocialAdmin(View):
    def get(self, request: HttpRequest):
        add_social_form = AdminSiteSocialModelForm()
        context = {
            'form': add_social_form
        }
        return render(request, 'admin_panel/site_setting/social_media/add_site_social_admin.html', context)

    def post(self, request: HttpRequest):
        add_social_form = AdminSiteSocialModelForm(request.POST)
        if add_social_form.is_valid():
            add_social_form.save()
            messages.info(request, 'شبکه اجتماعی با موفقیت ایجاد شد')
            return redirect(reverse('site_social_list_admin_page'))
        else:
            messages.error(request, 'مشکلی در ایجاد شبکه اجتماعی جدید به وجود آمده است')
        context = {
            'form': add_social_form
        }
        return render(request, 'admin_panel/site_setting/social_media/add_site_social_admin.html', context)


class EditAdminSiteSocial(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        socialId = kwargs.get('pk')
        current_social = get_object_or_404(SocialMedia, id=socialId)
        edit_social_form = AdminSiteSocialModelForm(instance=current_social)
        context = {
            'form': edit_social_form,
            'current_social': current_social
        }
        return render(request, 'admin_panel/site_setting/social_media/edit_site_social_admin.html', context)

    def post(self, request: HttpRequest, *args, **kwargs):
        socialId = kwargs.get('pk')
        current_social = get_object_or_404(SocialMedia, id=socialId)
        edit_social_form = AdminSiteSocialModelForm(request.POST, instance=current_social)
        if edit_social_form.is_valid():
            edit_social_form.save()
            messages.info(request, 'تغییرات با موفقیت ثبت شد')
            return redirect(reverse('site_social_list_admin_page'))
        else:
            messages.error(request, 'مشکلی در تغییر شبکه اجتماعی به وجود آمده است')
        context = {
            'form': edit_social_form,
            'current_social': current_social
        }
        return render(request, 'admin_panel/site_setting/social_media/edit_site_social_admin.html', context)


def delete_site_social(request: HttpRequest, pk):
    site_social = get_object_or_404(SocialMedia, pk=pk)

    if request.method == 'POST':
        site_social.delete()
        messages.info(request, 'تغییرات با موفقیت ثبت شد')
        return redirect(reverse('site_social_list_admin_page'))
    return redirect(reverse('edit_site_social_admin_page'))


class SiteTopProductAdminList(ListView):
    model = TopProduct
    template_name = 'admin_panel/site_setting/top_product/site_top_product_list_admin.html'
    paginate_by = 10

    def get_queryset(self):
        query = super().get_queryset()
        search_name = self.request.GET.get('search')
        lookup = Q(
            title__icontains=search_name) | Q(product__title__icontains=search_name)
        if search_name:
            site_tops = TopProduct.objects.filter(lookup).distinct()
            return site_tops
        else:
            return query.order_by('-id')


class AddSiteTopProductAdmin(View):
    def get(self, request: HttpRequest):
        add_top_form = AdminSiteTopProductModelForm()
        context = {
            'form': add_top_form
        }
        return render(request, 'admin_panel/site_setting/top_product/add_site_top_product_admin.html', context)

    def post(self, request: HttpRequest):
        add_top_form = AdminSiteTopProductModelForm(request.POST)
        if add_top_form.is_valid():
            add_top_form.save()
            messages.info(request, 'محصول برتر با موفقیت ایجاد شد')
            return redirect(reverse('site_top_product_list_admin_page'))
        else:
            messages.error(request, 'مشکلی در ایجاد محصول برتر جدید به وجود آمده است')
        context = {
            'form': add_top_form
        }
        return render(request, 'admin_panel/site_setting/top_product/add_site_top_product_admin.html', context)


class EditAdminSiteTopProduct(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        topId = kwargs.get('pk')
        current_top = get_object_or_404(TopProduct, id=topId)
        edit_top_form = AdminSiteTopProductModelForm(instance=current_top)
        context = {
            'form': edit_top_form,
            'current_top': current_top
        }
        return render(request, 'admin_panel/site_setting/top_product/edit_site_top_product_admin.html', context)

    def post(self, request: HttpRequest, *args, **kwargs):
        topId = kwargs.get('pk')
        current_top = get_object_or_404(TopProduct, id=topId)
        edit_top_form = AdminSiteTopProductModelForm(request.POST, instance=current_top)
        if edit_top_form.is_valid():
            edit_top_form.save()
            messages.info(request, 'تغییرات با موفقیت ثبت شد')
            return redirect(reverse('site_top_product_list_admin_page'))
        else:
            messages.error(request, 'مشکلی در تغییر محصولات برتر به وجود آمده است')
        context = {
            'form': edit_top_form,
            'current_top': current_top
        }
        return render(request, 'admin_panel/site_setting/top_product/edit_site_top_product_admin.html', context)


def delete_site_top_product(request: HttpRequest, pk):
    site_top_product = get_object_or_404(TopProduct, pk=pk)

    if request.method == 'POST':
        site_top_product.delete()
        messages.info(request, 'تغییرات با موفقیت ثبت شد')
        return redirect(reverse('site_top_product_list_admin_page'))
    return redirect(reverse('edit_site_top_product_admin_page'))


class SiteCategoryAdminList(ListView):
    model = SiteSettingCategory
    template_name = 'admin_panel/site_setting/category/site_category_list_admin.html'
    paginate_by = 10

    def get_queryset(self):
        query = super().get_queryset()
        search_name = self.request.GET.get('search')
        lookup = Q(
            title__icontains=search_name) | Q(product_category__title__icontains=search_name)
        if search_name:
            site_cats = SiteSettingCategory.objects.filter(lookup).distinct()
            return site_cats
        else:
            return query.order_by('-id')


class AddSiteCategoryAdmin(View):
    def get(self, request: HttpRequest):
        add_cat_form = AdminSiteCategoryModelForm()
        context = {
            'form': add_cat_form
        }
        return render(request, 'admin_panel/site_setting/category/add_site_category_admin.html', context)

    def post(self, request: HttpRequest):
        add_cat_form = AdminSiteCategoryModelForm(request.POST, request.FILES)
        if add_cat_form.is_valid():
            add_cat_form.save()
            messages.info(request, 'دسته بندی با موفقیت ایجاد شد')
            return redirect(reverse('site_category_list_admin_page'))
        else:
            messages.error(request, 'مشکلی در ایجاد دسته بندی جدید به وجود آمده است')
        context = {
            'form': add_cat_form
        }
        return render(request, 'admin_panel/site_setting/category/add_site_category_admin.html', context)


class EditAdminSiteCategory(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        catId = kwargs.get('pk')
        current_cat = get_object_or_404(SiteSettingCategory, id=catId)
        edit_cat_form = AdminSiteCategoryModelForm(instance=current_cat)
        context = {
            'form': edit_cat_form,
            'current_cat': current_cat
        }
        return render(request, 'admin_panel/site_setting/category/edit_site_category_admin.html', context)

    def post(self, request: HttpRequest, *args, **kwargs):
        catId = kwargs.get('pk')
        current_cat = get_object_or_404(SiteSettingCategory, id=catId)
        edit_cat_form = AdminSiteCategoryModelForm(request.POST, request.FILES, instance=current_cat)
        if edit_cat_form.is_valid():
            edit_cat_form.save()
            messages.info(request, 'تغییرات با موفقیت ثبت شد')
            return redirect(reverse('site_category_list_admin_page'))
        else:
            messages.error(request, 'مشکلی در تغییر دسته بندی به وجود آمده است')
        context = {
            'form': edit_cat_form,
            'current_cat': current_cat
        }
        return render(request, 'admin_panel/site_setting/category/edit_site_category_admin.html', context)


def delete_site_category(request: HttpRequest, pk):
    site_category = get_object_or_404(SiteSettingCategory, pk=pk)

    if request.method == 'POST':
        site_category.delete()
        messages.info(request, 'تغییرات با موفقیت ثبت شد')
        return redirect(reverse('site_category_list_admin_page'))
    return redirect(reverse('edit_site_category_admin_page'))


class SiteFooterBoxAdminList(ListView):
    model = FooterLinkBox
    template_name = 'admin_panel/site_setting/footer_box/site_footer_box_list_admin.html'
    paginate_by = 10

    def get_queryset(self):
        query = super().get_queryset()
        search_name = self.request.GET.get('search')
        lookup = Q(title__icontains=search_name)
        if search_name:
            site_fboxs = FooterLinkBox.objects.filter(lookup).distinct()
            return site_fboxs
        else:
            return query.order_by('-id')


class AddSiteFooterBoxAdmin(View):
    def get(self, request: HttpRequest):
        add_fbox_form = AdminSiteFooterBoxModelForm()
        context = {
            'form': add_fbox_form
        }
        return render(request, 'admin_panel/site_setting/footer_box/add_site_footer_box_admin.html', context)

    def post(self, request: HttpRequest):
        add_fbox_form = AdminSiteFooterBoxModelForm(request.POST)
        if add_fbox_form.is_valid():
            add_fbox_form.save()
            messages.info(request, 'باکس فوتر با موفقیت ایجاد شد')
            return redirect(reverse('site_footer_box_list_admin_page'))
        else:
            messages.error(request, 'مشکلی در ایجاد باکس فوتر جدید به وجود آمده است')
        context = {
            'form': add_fbox_form
        }
        return render(request, 'admin_panel/site_setting/footer_box/add_site_footer_box_admin.html', context)


class EditAdminSiteFooterBox(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        fboxId = kwargs.get('pk')
        current_fbox = get_object_or_404(FooterLinkBox, id=fboxId)
        edit_fbox_form = AdminSiteFooterBoxModelForm(instance=current_fbox)
        context = {
            'form': edit_fbox_form,
            'current_fbox': current_fbox
        }
        return render(request, 'admin_panel/site_setting/footer_box/edit_site_footer_box_admin.html', context)

    def post(self, request: HttpRequest, *args, **kwargs):
        fboxId = kwargs.get('pk')
        current_fbox = get_object_or_404(FooterLinkBox, id=fboxId)
        edit_fbox_form = AdminSiteFooterBoxModelForm(request.POST, instance=current_fbox)
        if edit_fbox_form.is_valid():
            edit_fbox_form.save()
            messages.info(request, 'تغییرات با موفقیت ثبت شد')
            return redirect(reverse('site_footer_box_list_admin_page'))
        else:
            messages.error(request, 'مشکلی در تغییر باکس فوتر به وجود آمده است')
        context = {
            'form': edit_fbox_form,
            'current_fbox': current_fbox
        }
        return render(request, 'admin_panel/site_setting/footer_box/edit_site_footer_box_admin.html', context)


def delete_site_footer_box(request: HttpRequest, pk):
    site_footer_box = get_object_or_404(FooterLinkBox, pk=pk)

    if request.method == 'POST':
        site_footer_box.delete()
        messages.info(request, 'تغییرات با موفقیت ثبت شد')
        return redirect(reverse('site_footer_box_list_admin_page'))
    return redirect(reverse('edit_site_footer_box_admin_page'))


class SiteFooterLinkAdminList(ListView):
    model = FooterLink
    template_name = 'admin_panel/site_setting/footer_link/site_footer_link_list_admin.html'
    paginate_by = 10

    def get_queryset(self):
        query = super().get_queryset()
        search_name = self.request.GET.get('search')
        lookup = Q(title__icontains=search_name)
        if search_name:
            site_flink = FooterLink.objects.filter(lookup).distinct()
            return site_flink
        else:
            return query.order_by('-id')


class AddSiteFooterLinkAdmin(View):
    def get(self, request: HttpRequest):
        add_flink_form = AdminSiteFooterLinkModelForm()
        context = {
            'form': add_flink_form
        }
        return render(request, 'admin_panel/site_setting/footer_link/add_site_footer_link_admin.html', context)

    def post(self, request: HttpRequest):
        add_flink_form = AdminSiteFooterLinkModelForm(request.POST)
        if add_flink_form.is_valid():
            add_flink_form.save()
            messages.info(request, 'باکس فوتر با موفقیت ایجاد شد')
            return redirect(reverse('site_footer_link_list_admin_page'))
        else:
            messages.error(request, 'مشکلی در ایجاد لینک فوتر جدید به وجود آمده است')
        context = {
            'form': add_flink_form
        }
        return render(request, 'admin_panel/site_setting/footer_link/add_site_footer_link_admin.html', context)


class EditAdminSiteFooterLink(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        flinkId = kwargs.get('pk')
        current_flink = get_object_or_404(FooterLink, id=flinkId)
        edit_flink_form = AdminSiteFooterLinkModelForm(instance=current_flink)
        context = {
            'form': edit_flink_form,
            'current_flink': current_flink
        }
        return render(request, 'admin_panel/site_setting/footer_link/edit_site_footer_link_admin.html', context)

    def post(self, request: HttpRequest, *args, **kwargs):
        flinkId = kwargs.get('pk')
        current_flink = get_object_or_404(FooterLink, id=flinkId)
        edit_flink_form = AdminSiteFooterLinkModelForm(request.POST, instance=current_flink)
        if edit_flink_form.is_valid():
            edit_flink_form.save()
            messages.info(request, 'تغییرات با موفقیت ثبت شد')
            return redirect(reverse('site_footer_link_list_admin_page'))
        else:
            messages.error(request, 'مشکلی در تغییر لینک فوتر به وجود آمده است')
        context = {
            'form': edit_flink_form,
            'current_flink': current_flink
        }
        return render(request, 'admin_panel/site_setting/footer_link/edit_site_footer_link_admin.html', context)


def delete_site_footer_link(request: HttpRequest, pk):
    site_footer_link = get_object_or_404(FooterLink, pk=pk)

    if request.method == 'POST':
        site_footer_link.delete()
        messages.info(request, 'تغییرات با موفقیت ثبت شد')
        return redirect(reverse('site_footer_link_list_admin_page'))
    return redirect(reverse('edit_site_footer_link_admin_page'))


class OrderAdminList(ListView):
    model = Order
    template_name = 'admin_panel/orders/order_list_admin.html'
    paginate_by = 15

    def convert_to_gregorian(self, jalali_date_str):
        try:
            # Parse the Jalali date string
            jalali_date = jdatetime.datetime.strptime(jalali_date_str, '%Y/%m/%d')

            # Convert Jalali date to a Gregorian date string
            g_date_str = jalali_date.togregorian().strftime('%Y-%m-%d')

            return g_date_str
        except Exception as e:
            print(f"Error converting date: {e}")
            return None

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        counts = {
            'default': Order.objects.filter(is_paid=True).count(),
            'waiting': Order.objects.filter(is_paid=True, status='انتظار').count(),
            'processing': Order.objects.filter(is_paid=True, status='در حال پردازش').count(),
            'sent': Order.objects.filter(is_paid=True, status='ارسال شده').count(),
        }
        context['order'] = self.request.GET.get('order', 'default')
        context['order_detail'] = OrderDetail.objects.filter()
        context['counts'] = counts
        return context

    def get_queryset(self):
        query = super().get_queryset()
        orders = self.request.GET.get('order', 'default')
        search_name = self.request.GET.get('search')
        search_date = self.request.GET.get('search-date')
        lookup = Q()
        lookup_search = Q(orderdetail__product__title__icontains=search_name) | Q(
            user__first_name__icontains=search_name) | Q(address__province__icontains=search_name) | Q(
            address__city__icontains=search_name) | Q(address__full_name__icontains=search_name)

        if search_date:
            try:
                gregorian_date_str = self.convert_to_gregorian(search_date)
                print(gregorian_date_str)
                if gregorian_date_str:
                    lookup_date = Q(payment_date__exact=gregorian_date_str)
                    orders = Order.objects.filter(lookup_date).distinct()
                    return orders
            except Exception as e:
                print(f"Error parsing date from URL: {e}")

        if search_name:
            orders = Order.objects.filter(lookup_search).distinct()
            return orders

        if orders == 'waiting':
            lookup |= Q(status__iexact='انتظار')
            return query.filter(lookup).distinct()
        elif orders == 'processing':
            lookup |= Q(status__iexact='در حال پردازش')
            return query.filter(lookup).distinct()
        elif orders == 'sent':
            lookup |= Q(status__iexact='ارسال شده')
            return query.filter(lookup).distinct()
        return query.filter(is_paid=True).order_by('-id')


class EditOrderAdmin(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        orderId = kwargs.get('pk')
        current_order = get_object_or_404(Order, id=orderId)
        edit_order_form = AdminOrderModelForm(instance=current_order)
        users_purchases = Order.objects.filter(is_paid=True).annotate(count=Count('is_paid'))
        order_detail = OrderDetail.objects.filter(order_id=current_order.id)

        context = {
            'form': edit_order_form,
            'current_order': current_order,
            'users_purchases': users_purchases,
            'order_detail': order_detail,
        }
        return render(request, 'admin_panel/orders/edit_order_admin.html', context)

    def post(self, request: HttpRequest, *args, **kwargs):
        orderId = kwargs.get('pk')
        current_order = get_object_or_404(Order, id=orderId)
        edit_order_form = AdminOrderModelForm(request.POST, instance=current_order)
        users_purchases = User.objects.filter(order__is_paid=True).annotate(count=Count('order'))
        order_detail = OrderDetail.objects.filter(order_id=current_order.id)
        if edit_order_form.is_valid():
            edit_order_form.save()
            messages.info(request, 'تغییرات با موفقیت ثبت شد')
            return redirect(reverse('order_list_admin_page'))
        else:
            messages.error(request, 'مشکلی در تغییر سفارش به وجود آمده است')
        context = {
            'form': edit_order_form,
            'current_order': current_order,
            'users_purchases': users_purchases,
            'order_detail': order_detail
        }
        return render(request, 'admin_panel/orders/edit_order_admin.html', context)


def delete_order(request: HttpRequest, pk):
    order = get_object_or_404(Order, pk=pk)

    order.delete()
    messages.info(request, 'تغییرات با موفقیت ثبت شد')
    return redirect(reverse('order_list_admin_page'))


def delete_order_detail(request: HttpRequest, pk):
    order_detail = get_object_or_404(OrderDetail, pk=pk)

    order_detail.delete()
    messages.info(request, 'تغییرات با موفقیت ثبت شد')
    return redirect(reverse('order_list_admin_page'))


def invoice_order(request: HttpRequest, pk):
    current_order = get_object_or_404(Order, pk=pk)
    site_setting = get_object_or_404(SiteSetting)
    order_detail = OrderDetail.objects.filter(order_id=current_order.id)
    context = {
        'current_order': current_order,
        'site_setting': site_setting,
        'order_detail': order_detail,
    }
    return render(request, 'admin_panel/orders/invoice_order.html', context)


class WholesaleAdminList(ListView):
    model = Wholesale
    template_name = 'admin_panel/orders/wholesale/wholesale_list_admin.html'
    paginate_by = 10

    def convert_to_gregorian(self, jalali_date_str):
        try:
            # Parse the Jalali date string
            jalali_date = jdatetime.datetime.strptime(jalali_date_str, '%Y/%m/%d')

            # Convert Jalali date to a Gregorian date string
            g_date_str = jalali_date.togregorian().strftime('%Y-%m-%d')

            return g_date_str
        except Exception as e:
            print(f"Error converting date: {e}")
            return None

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        counts = {
            'default': Wholesale.objects.filter(payment_status=True).count(),
            'waiting': Wholesale.objects.filter(payment_status=True, status='انتظار').count(),
            'processing': Wholesale.objects.filter(payment_status=True, status='در حال پردازش').count(),
            'sent': Wholesale.objects.filter(payment_status=True, status='ارسال شده').count(),
        }
        context['wholesale'] = self.request.GET.get('order', 'default')
        context['counts'] = counts
        return context

    def get_queryset(self):
        query = super().get_queryset()
        wholes = self.request.GET.get('order', 'default')
        search_name = self.request.GET.get('search')
        search_date = self.request.GET.get('search-date')
        lookup = Q()
        lookup_search = Q(full_name__icontains=search_name) | Q(company_name__icontains=search_name) | Q(
            email__icontains=search_name) | Q(product__icontains=search_name) | Q(
            full_address__icontains=search_name) | Q(phone_number__icontains=search_name)

        if search_date:
            try:
                gregorian_date_str = self.convert_to_gregorian(search_date)
                print(gregorian_date_str)
                if gregorian_date_str:
                    lookup_date = Q(order_date__exact=gregorian_date_str)
                    wholes = Wholesale.objects.filter(lookup_date).distinct()
                    return wholes
            except Exception as e:
                print(f"Error parsing date from URL: {e}")

        if search_name:
            wholes = Wholesale.objects.filter(lookup_search).distinct()
            return wholes

        if wholes == 'waiting':
            lookup |= Q(status__iexact='انتظار')
            return query.filter(lookup).distinct()
        elif wholes == 'processing':
            lookup |= Q(status__iexact='در حال پردازش')
            return query.filter(lookup).distinct()
        elif wholes == 'sent':
            lookup |= Q(status__iexact='ارسال شده')
            return query.filter(lookup).distinct()
        return query.all()


class AddWholesaleAdmin(View):
    def get(self, request: HttpRequest):
        add_whole_form = AdminWholesaleModelForm()
        context = {
            'form': add_whole_form
        }
        return render(request, 'admin_panel/orders/wholesale/add_wholesale_admin.html', context)

    def post(self, request: HttpRequest):
        add_whole_form = AdminWholesaleModelForm(request.POST)
        if add_whole_form.is_valid():
            add_whole_form.save()
            messages.info(request, 'سفارش با موفقیت ایجاد شد')
            return redirect(reverse('wholesale_list_admin_page'))
        else:
            messages.error(request, 'مشکلی در ایجاد سفارش جدید به وجود آمده است')
        context = {
            'form': add_whole_form
        }
        return render(request, 'admin_panel/orders/wholesale/add_wholesale_admin.html', context)


class EditAdminWholesale(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        wholeId = kwargs.get('pk')
        current_whole = get_object_or_404(Wholesale, id=wholeId)
        edit_whole_form = AdminWholesaleModelForm(instance=current_whole)
        context = {
            'form': edit_whole_form,
            'current_whole': current_whole
        }
        return render(request, 'admin_panel/orders/wholesale/edit_wholesale_admin.html', context)

    def post(self, request: HttpRequest, *args, **kwargs):
        wholeId = kwargs.get('pk')
        current_whole = get_object_or_404(Wholesale, id=wholeId)
        edit_whole_form = AdminWholesaleModelForm(request.POST, instance=current_whole)
        if edit_whole_form.is_valid():
            edit_whole_form.save()
            messages.info(request, 'تغییرات با موفقیت ثبت شد')
            return redirect(reverse('wholesale_list_admin_page'))
        else:
            messages.error(request, 'مشکلی در تغییر سفارش به وجود آمده است')
        context = {
            'form': edit_whole_form,
            'current_whole': current_whole
        }
        return render(request, 'admin_panel/orders/wholesale/edit_wholesale_admin.html', context)


def delete_wholesale(request: HttpRequest, pk):
    wholesale = get_object_or_404(Wholesale, pk=pk)

    wholesale.delete()
    messages.info(request, 'تغییرات با موفقیت ثبت شد')
    return redirect(reverse('wholesale_list_admin_page'))


def invoice_wholesale(request: HttpRequest, pk):
    site_setting = get_object_or_404(SiteSetting)
    wholesale = get_object_or_404(Wholesale, pk=pk)
    context = {
        'site_setting': site_setting,
        'wholesale': wholesale,
    }
    return render(request, 'admin_panel/orders/wholesale/invoice_wholesale.html', context)


class UserAdminList(ListView):
    model = User
    template_name = 'admin_panel/user/user_list_admin.html'
    paginate_by = 20

    def get_queryset(self):
        query = super().get_queryset()
        search_name = self.request.GET.get('search')
        lookup = Q(full_name__icontains=search_name) | Q(first_name__icontains=search_name) | Q(
            last_name__icontains=search_name) | Q(username__icontains=search_name) | Q(
            phone_number__icontains=search_name) | Q(email__icontains=search_name)
        if search_name:
            users = User.objects.filter(lookup).distinct()
            return users
        else:
            return query.order_by('-is_superuser', '-is_staff', '-is_active', '-date_joined')


class AddUserAdmin(View):
    def get(self, request: HttpRequest):
        add_user_form = AddUserAdminForm()
        context = {
            'form': add_user_form
        }
        return render(request, 'admin_panel/user/add_user_admin.html', context)

    def post(self, request: HttpRequest):
        add_user_form = AddUserAdminForm(request.POST)
        if add_user_form.is_valid():
            user_username = add_user_form.cleaned_data.get('username')
            user_fullname = add_user_form.cleaned_data.get('full_name')
            user_email = add_user_form.cleaned_data.get('email')
            user_phonenumber = add_user_form.cleaned_data.get('phone_number')
            user_password = add_user_form.cleaned_data.get('password')
            query = Q(username__iexact=user_username) | Q(phone_number__iexact=user_phonenumber)
            user: User = User.objects.filter(query).exists()
            if user:
                messages.error(request, 'نام کاربری یا شماره موبایل از قبل وارد شده است. لطفا دوباره امتحان کنید')
            else:
                new_user = User(
                    full_name=user_fullname,
                    username=user_username,
                    phone_number=user_phonenumber,
                    email=user_email,
                    is_active=True,
                    is_staff=True,
                    date_joined=timezone.now()
                )
                new_user.set_password(user_password)
                new_user.save()
                messages.info(request, 'کاربر با موفقیت ایجاد شد')
                return redirect(reverse('user_list_admin_page'))
        else:
            messages.error(request, 'مشکلی در ایجاد کاربر جدید به وجود آمده است')
        context = {
            'form': add_user_form
        }
        return render(request, 'admin_panel/user/add_user_admin.html', context)


class LoginUserAdmin(View):

    def get(self, request: HttpRequest):
        login_user_form = LoginUserAdminForm()
        context = {
            'form': login_user_form
        }
        return render(request, 'admin_panel/user/login_user_admin.html', context)

    def post(self, request: HttpRequest):
        login_user_form = LoginUserAdminForm(request.POST)
        if login_user_form.is_valid():
            user_username = login_user_form.cleaned_data.get('username')
            user_password = login_user_form.cleaned_data.get('password')
            user: User = User.objects.filter(username__iexact=user_username).first()
            if user:
                if not user.is_staff:
                    login_user_form.add_error('username', 'حساب کاربری شما فعال نشده است')
                else:
                    is_correct_password = user.check_password(user_password)
                    if is_correct_password:
                        login(request, user)
                        return redirect(reverse('index_admin_page'))
                    else:
                        login_user_form.add_error('password', 'کلمه عبور اشتباه میباشد')
            else:
                login_user_form.add_error('username', 'کاربری با مشخصات وارد شده یافت نشد')

        context = {
            'form': login_user_form
        }
        return render(request, 'admin_panel/user/login_user_admin.html', context)


class ChangePasswordUserAdmin(View):
    def get(self, request: HttpRequest):
        change_pass_form = ChangePasswordUserAdminForm()
        context = {
            'form': change_pass_form
        }
        return render(request, 'admin_panel/user/change_password_admin.html', context)

    def post(self, request: HttpRequest):
        change_pass_form = ChangePasswordUserAdminForm(request.POST)
        if change_pass_form.is_valid():
            user: User = User.objects.filter(id=request.user.id).first()
            new_pass = change_pass_form.cleaned_data.get('new_password')
            current_pass = change_pass_form.cleaned_data.get('current_password')
            if user.check_password(current_pass):
                user.set_password(new_pass)
                user.save()
                logout(request)
                return redirect(reverse('login_user_admin_page'))
            else:
                change_pass_form.add_error('current_password', 'کلمه عبور وارد شده اشتباه می باشد')

        context = {
            'form': change_pass_form
        }
        return render(request, 'admin_panel/user/change_password_admin.html', context)


def logout_user_admin(request):
    logout(request)
    return redirect(reverse('login_user_admin_page'))


class EditAdminUser(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        userId = kwargs.get('pk')
        current_user = get_object_or_404(User, id=userId)
        edit_user_form = AdminUserModelForm(instance=current_user)
        address = Address.objects.filter(user=current_user.id)
        used_coupons = Coupon.objects.filter(used_by=request.user)
        context = {
            'form': edit_user_form,
            'current_user': current_user,
            'address': address,
            'used_coupons': used_coupons
        }
        return render(request, 'admin_panel/user/edit_user_admin.html', context)

    def post(self, request: HttpRequest, *args, **kwargs):
        userId = kwargs.get('pk')
        current_user = get_object_or_404(User, id=userId)
        edit_user_form = AdminUserModelForm(request.POST, instance=current_user)
        address = Address.objects.filter(user=userId)
        if edit_user_form.is_valid():
            edit_user_form.save()
            messages.info(request, 'تغییرات با موفقیت ثبت شد')
            return redirect(reverse('user_list_admin_page'))
        else:
            messages.error(request, 'مشکلی در تغییر اطلاعات کاربر به وجود آمده است')
        context = {
            'form': edit_user_form,
            'current_user': current_user,
            'address': address
        }
        return render(request, 'admin_panel/user/edit_user_admin.html', context)


def delete_user(request: HttpRequest, pk):
    user = get_object_or_404(User, pk=pk)

    user.delete()
    messages.info(request, 'تغییرات با موفقیت ثبت شد')
    return redirect(reverse('user_list_admin_page'))


class AddressAdminList(ListView):
    model = Address
    template_name = 'admin_panel/user/address/address_list_admin.html'
    paginate_by = 15

    def get_queryset(self):
        query = super().get_queryset()
        search_name = self.request.GET.get('search')
        lookup = Q(
            full_name__icontains=search_name) | Q(city__icontains=search_name) | Q(province__icontains=search_name) | Q(
            phone_number__icontains=search_name) | Q(phone_number__icontains=search_name) | Q(
            user__username__icontains=search_name) | Q(user__full_name__icontains=search_name)
        if search_name:
            addresses = Address.objects.filter(lookup).distinct()
            return addresses
        else:
            return query.order_by('-id')


class AddAddressAdmin(View):
    def get(self, request: HttpRequest):
        add_address_form = AdminAddressModelForm()
        context = {
            'form': add_address_form
        }
        return render(request, 'admin_panel/user/address/add_address_admin.html', context)

    def post(self, request: HttpRequest):
        add_address_form = AdminAddressModelForm(request.POST)
        if add_address_form.is_valid():
            add_address_form.save()
            messages.info(request, 'آدرس با موفقیت ایجاد شد')
            return redirect(reverse('address_list_admin_page'))
        else:
            messages.error(request, 'مشکلی در ایجاد آدرس جدید به وجود آمده است')
        context = {
            'form': add_address_form
        }
        return render(request, 'admin_panel/user/address/add_address_admin.html', context)


class EditAdminAddress(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        addId = kwargs.get('pk')
        current_address = get_object_or_404(Address, id=addId)
        edit_address_form = AdminAddressModelForm(instance=current_address)
        context = {
            'form': edit_address_form,
            'current_address': current_address
        }
        return render(request, 'admin_panel/user/address/edit_address_admin.html', context)

    def post(self, request: HttpRequest, *args, **kwargs):
        addId = kwargs.get('pk')
        current_address = get_object_or_404(Address, id=addId)
        edit_address_form = AdminAddressModelForm(request.POST, instance=current_address)
        if edit_address_form.is_valid():
            edit_address_form.save()
            messages.info(request, 'تغییرات با موفقیت ثبت شد')
            return redirect(reverse('address_list_admin_page'))
        else:
            messages.error(request, 'مشکلی در تغییر آدرس به وجود آمده است')
        context = {
            'form': edit_address_form,
            'current_address': current_address
        }
        return render(request, 'admin_panel/user/address/edit_address_admin.html', context)


def delete_address(request: HttpRequest, pk):
    address = get_object_or_404(Address, pk=pk)

    if request.method == 'POST':
        address.delete()
        messages.info(request, 'تغییرات با موفقیت ثبت شد')
        return redirect(reverse('address_list_admin_page'))
    return redirect(reverse('edit_address_admin_page'))


class WalletAdminList(ListView):
    model = Wallet
    template_name = 'admin_panel/wallet/wallet_list_admin.html'
    paginate_by = 15

    def get_queryset(self):
        query = super().get_queryset()
        search_name = self.request.GET.get('search')
        lookup = Q(user__full_name__icontains=search_name) | Q(
            user__phone_number__icontains=search_name)
        if search_name:
            wallets = Wallet.objects.filter(lookup).distinct()
            return wallets
        else:
            return query.order_by('-id')


class AddWalletAdmin(View):
    def get(self, request: HttpRequest):
        add_wallet_form = AdminWalletModelForm()
        context = {
            'form': add_wallet_form
        }
        return render(request, 'admin_panel/wallet/add_wallet_admin.html', context)

    def post(self, request: HttpRequest):
        add_wallet_form = AdminWalletModelForm(request.POST)
        if add_wallet_form.is_valid():
            add_wallet_form.save()
            messages.info(request, 'کیف پول با موفقیت ایجاد شد')
            return redirect(reverse('wallet_list_admin_page'))
        else:
            messages.error(request, 'مشکلی در ایجاد کیف پول جدید به وجود آمده است')
        context = {
            'form': add_wallet_form
        }
        return render(request, 'admin_panel/wallet/add_wallet_admin.html', context)


class EditAdminWallet(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        walletId = kwargs.get('pk')
        current_wallet = get_object_or_404(Wallet, id=walletId)
        edit_wallet_form = AdminWalletModelForm(instance=current_wallet)
        context = {
            'form': edit_wallet_form,
            'current_wallet': current_wallet
        }
        return render(request, 'admin_panel/wallet/edit_wallet_admin.html', context)

    def post(self, request: HttpRequest, *args, **kwargs):
        walletId = kwargs.get('pk')
        current_wallet = get_object_or_404(Wallet, id=walletId)
        edit_wallet_form = AdminWalletModelForm(request.POST, instance=current_wallet)
        if edit_wallet_form.is_valid():
            edit_wallet_form.save()
            messages.info(request, 'تغییرات با موفقیت ثبت شد')
            return redirect(reverse('wallet_list_admin_page'))
        else:
            messages.error(request, 'مشکلی در تغییر کیف پول به وجود آمده است')
        context = {
            'form': edit_wallet_form,
            'current_wallet': current_wallet
        }
        return render(request, 'admin_panel/wallet/edit_wallet_admin.html', context)


def delete_wallet(request: HttpRequest, pk):
    wallet = get_object_or_404(Wallet, pk=pk)

    if request.method == 'POST':
        wallet.delete()
        messages.info(request, 'تغییرات با موفقیت ثبت شد')
        return redirect(reverse('wallet_list_admin_page'))
    return redirect(reverse('edit_wallet_admin_page'))


class TransactionWalletAdminList(ListView):
    model = Transaction
    template_name = 'admin_panel/wallet/transaction/transaction_wallet_list_admin.html'
    paginate_by = 15

    def get_queryset(self):
        query = super().get_queryset()
        search_name = self.request.GET.get('search')
        lookup = Q(user__full_name__icontains=search_name) | Q(
            user__phone_number__icontains=search_name)
        if search_name:
            transactions = Transaction.objects.filter(lookup).distinct()
            return transactions
        else:
            return query.order_by('-id')


class AddTransactionWalletAdmin(View):
    def get(self, request: HttpRequest):
        add_tr_form = AdminTransactionWalletModelForm()
        context = {
            'form': add_tr_form
        }
        return render(request, 'admin_panel/wallet/transaction/add_transaction_wallet_admin.html', context)

    def post(self, request: HttpRequest):
        add_tr_form = AdminTransactionWalletModelForm(request.POST)
        if add_tr_form.is_valid():
            add_tr_form.save()
            messages.info(request, 'تراکنش با موفقیت ایجاد شد')
            return redirect(reverse('transaction_wallet_list_admin_page'))
        else:
            messages.error(request, 'مشکلی در ایجاد تراکنش جدید به وجود آمده است')
        context = {
            'form': add_tr_form
        }
        return render(request, 'admin_panel/wallet/transaction/add_transaction_wallet_admin.html', context)


class EditAdminTransactionWallet(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        trId = kwargs.get('pk')
        current_transaction = get_object_or_404(Transaction, id=trId)
        edit_tr_form = AdminTransactionWalletModelForm(instance=current_transaction)
        context = {
            'form': edit_tr_form,
            'current_transaction': current_transaction
        }
        return render(request, 'admin_panel/wallet/transaction/edit_transaction_wallet_admin.html', context)

    def post(self, request: HttpRequest, *args, **kwargs):
        trId = kwargs.get('pk')
        current_transaction = get_object_or_404(Transaction, id=trId)
        edit_tr_form = AdminTransactionWalletModelForm(request.POST, instance=current_transaction)
        if edit_tr_form.is_valid():
            edit_tr_form.save()
            messages.info(request, 'تغییرات با موفقیت ثبت شد')
            return redirect(reverse('transaction_wallet_list_admin_page'))
        else:
            messages.error(request, 'مشکلی در تغییر تراکنش به وجود آمده است')
        context = {
            'form': edit_tr_form,
            'current_transaction': current_transaction
        }
        return render(request, 'admin_panel/wallet/transaction/edit_transaction_wallet_admin.html', context)


def delete_transaction_wallet(request: HttpRequest, pk):
    transaction = get_object_or_404(Transaction, pk=pk)

    if request.method == 'POST':
        transaction.delete()
        messages.info(request, 'تغییرات با موفقیت ثبت شد')
        return redirect(reverse('transaction_wallet_list_admin_page'))
    return redirect(reverse('edit_transaction_wallet_admin_page'))


class WalletSettingAdminList(ListView):
    model = WalletSetting
    template_name = 'admin_panel/wallet/wallet_setting/wallet_setting_list_admin.html'
    paginate_by = 15

    def get_queryset(self):
        query = super().get_queryset()
        return query.order_by('-id')


class EditWalletSetting(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        settingId = kwargs.get('pk')
        current_setting = get_object_or_404(WalletSetting, id=settingId)
        edit_setting_form = AdminWalletSettingModelForm(instance=current_setting)
        context = {
            'form': edit_setting_form,
            'current_setting': current_setting
        }
        return render(request, 'admin_panel/wallet/wallet_setting/edit_wallet_setting_admin.html', context)

    def post(self, request: HttpRequest, *args, **kwargs):
        settingId = kwargs.get('pk')
        current_setting = get_object_or_404(WalletSetting, id=settingId)
        edit_setting_form = AdminWalletSettingModelForm(request.POST, instance=current_setting)
        if edit_setting_form.is_valid():
            edit_setting_form.save()
            messages.info(request, 'تغییرات با موفقیت ثبت شد')
            return redirect(reverse('wallet_setting_list_admin_page'))
        else:
            messages.error(request, 'مشکلی در تغییر تنظیمات به وجود آمده است')
        context = {
            'form': edit_setting_form,
            'current_setting': current_setting
        }
        return render(request, 'admin_panel/wallet/wallet_setting/edit_wallet_setting_admin.html', context)


class CouponAdminList(ListView):
    model = Coupon
    template_name = 'admin_panel/coupon/coupon_list_admin.html'
    paginate_by = 15

    def get_queryset(self):
        query = super().get_queryset()
        search_name = self.request.GET.get('search')
        lookup = Q(code__icontains=search_name) | Q(discount__gte=search_name) | Q(
            used_by__username__icontains=search_name)
        if search_name:
            coupons = Coupon.objects.filter(lookup).distinct()
            return coupons
        else:
            return query.order_by('-id')


class AddCouponAdmin(View):
    def get(self, request: HttpRequest):
        add_coupon_form = AdminCouponModelForm()
        context = {
            'form': add_coupon_form
        }
        return render(request, 'admin_panel/coupon/add_coupon_admin.html', context)

    def post(self, request: HttpRequest):
        add_coupon_form = AdminCouponModelForm(request.POST)
        if add_coupon_form.is_valid():
            add_coupon_form.save()
            messages.info(request, 'کد تخفیف با موفقیت ایجاد شد')
            return redirect(reverse('coupon_list_admin_page'))
        else:
            messages.error(request, 'مشکلی در ایجاد کد تخفیف جدید به وجود آمده است')
        context = {
            'form': add_coupon_form
        }
        return render(request, 'admin_panel/coupon/add_coupon_admin.html', context)


class EditAdminCoupon(View):
    def get(self, request: HttpRequest, *args, **kwargs):
        couponId = kwargs.get('pk')
        current_coupon = get_object_or_404(Coupon, id=couponId)
        edit_coupon_form = AdminCouponModelForm(instance=current_coupon)
        context = {
            'form': edit_coupon_form,
            'current_coupon': current_coupon
        }
        return render(request, 'admin_panel/coupon/edit_coupon_admin.html', context)

    def post(self, request: HttpRequest, *args, **kwargs):
        couponId = kwargs.get('pk')
        current_coupon = get_object_or_404(Coupon, id=couponId)
        edit_coupon_form = AdminCouponModelForm(request.POST, instance=current_coupon)
        if edit_coupon_form.is_valid():
            edit_coupon_form.save()
            messages.info(request, 'تغییرات با موفقیت ثبت شد')
            return redirect(reverse('coupon_list_admin_page'))
        else:
            messages.error(request, 'مشکلی در تغییر کد تخفیف به وجود آمده است')
        context = {
            'form': edit_coupon_form,
            'current_coupon': current_coupon
        }
        return render(request, 'admin_panel/coupon/edit_coupon_admin.html', context)


def delete_coupon(request: HttpRequest, pk):
    coupon = get_object_or_404(Coupon, pk=pk)

    if request.method == 'POST':
        coupon.delete()
        messages.info(request, 'تغییرات با موفقیت ثبت شد')
        return redirect(reverse('coupon_list_admin_page'))
    return redirect(reverse('edit_coupon_admin_page'))
