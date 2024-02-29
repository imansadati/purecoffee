from django.db import models
from django.db.models import Sum
from django.urls import reverse

from account_module.models import User
from product_module.models import Product, ProductColor, ProductGrind, Coupon

# Create your models here.


STATUS_CHOICES = (
    ('SHIPPED', 'ارسال شده'),
    ('PENDING', 'انتظار'),
    ('PROCESSING', 'در حال پردازش'),
)


class Order(models.Model):
    class OrderStatus(models.TextChoices):
        shipped = 'ارسال شده', 'ارسال شده'
        pending = 'انتظار', 'انتظار'
        processing = 'در حال پردازش', 'در حال پردازش'

    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    address = models.ForeignKey('Address', on_delete=models.CASCADE, null=True, blank=True, verbose_name='آدرس')
    is_paid = models.BooleanField(verbose_name='نهایی شده / نشده')
    payment_date = models.DateField(null=True, blank=True, verbose_name='تاریخ پرداخت')
    status = models.CharField(max_length=30, verbose_name='وضعیت سفارش', choices=OrderStatus.choices,
                              default=OrderStatus.pending)
    payable_amount = models.BigIntegerField(null=True, blank=True, verbose_name='قیمت نهایی پرداخت شده')
    total_amount = models.BigIntegerField(null=True, blank=True, verbose_name='قیمت کل')
    transaction_amount = models.BigIntegerField(null=True, blank=True, verbose_name='مبلغ تراکنش کیف پول')
    coupon = models.CharField(max_length=100, null=True, blank=True, verbose_name='کد تخفیف استفاده شده')

    # def save(self, *args, **kwargs):
    #     if self.payable_amount < 0:
    #         self.payable_amount = 0
    #     else:
    #         pass
    #     super(Order, self).save()

    # def calculate_product_count(self):
    #     return self.orderdetail_set.aggregate(total_count=Sum('count'))['total_count'] or 0

    def calculate_total_price(self):
        total_amount = 0
        if self.is_paid:
            for order_detail in self.orderdetail_set.all():
                total_amount += order_detail.final_price
        else:
            for order_detail in self.orderdetail_set.all():
                total_amount += order_detail.product.price * order_detail.count
        return total_amount

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبد های خرید کاربران'

    def __str__(self):
        return str(self.user)


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='سبد خرید')
    create_added = models.DateTimeField(auto_now_add=True, editable=False,
                                        verbose_name='زمان اضافه شدن محصول به سبد خرید')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    color = models.CharField(max_length=50, verbose_name='رنگ محصول', null=True, blank=True)
    grind = models.CharField(max_length=50, verbose_name='آسیاب محصول', null=True, blank=True)
    final_price = models.IntegerField(null=True, blank=True, verbose_name='قیمت نهایی تکی محصول')
    count = models.IntegerField(verbose_name='تعداد')

    def get_total_price(self):
        return self.count * self.product.price

    def get_absolute_url_admin(self):
        return reverse('edit_product_admin_page', args=[self.product.id])

    class Meta:
        verbose_name = 'جزییات سبد خرید'
        verbose_name_plural = 'لیست جزییات سبدهای خرید'

    def __str__(self):
        return str(self.order)


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='کاربر')
    full_name = models.CharField(max_length=100, verbose_name='نام و نام خانوادگی')
    phone_number = models.CharField(max_length=11, verbose_name='شماره موبایل')
    province = models.CharField(max_length=100, verbose_name='استان')
    city = models.CharField(max_length=100, verbose_name='شهر')
    exact_address = models.TextField(verbose_name='آدرس دقیق')
    plaque = models.PositiveIntegerField(verbose_name='پلاک')
    postal_code = models.PositiveBigIntegerField(blank=True, null=True, verbose_name='کد پستی')

    def __str__(self):
        return self.phone_number


class Wholesale(models.Model):
    class WholesaleStatus(models.TextChoices):
        shipped = 'ارسال شده', 'ارسال شده'
        pending = 'انتظار', 'انتظار'
        processing = 'در حال پردازش', 'در حال پردازش'

    full_name = models.CharField(max_length=100, verbose_name='نام و نام خانوادگی')
    company_name = models.CharField(max_length=100, null=True, blank=True, verbose_name='نام شرکت')
    phone_number = models.CharField(max_length=30, verbose_name='شماره موبایل')
    landline_phone = models.CharField(max_length=15, null=True, blank=True, verbose_name='شماره ثابت')
    email = models.EmailField(null=True, blank=True, verbose_name='ایمیل')
    full_address = models.TextField(verbose_name='آدرس کامل')
    product = models.TextField(verbose_name='جزییات کامل سفارش')
    statement = models.PositiveBigIntegerField(null=True, blank=True, verbose_name='بیانه')
    total_amount_payable = models.PositiveBigIntegerField(verbose_name='کل مبلغ قابل پرداخت')
    total_amount_paid = models.PositiveBigIntegerField(verbose_name='کل مبلغ پرداخت شده')
    order_date = models.DateField(auto_now_add=True, verbose_name='تاریخ سفارش')
    status = models.CharField(choices=WholesaleStatus.choices, max_length=30, default=WholesaleStatus.pending,
                              verbose_name='وضعیت')
    payment_status = models.BooleanField(default=False, verbose_name='پرداخت شده / نشده')

    def __str__(self):
        return self.full_name
