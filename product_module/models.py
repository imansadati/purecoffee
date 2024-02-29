from ckeditor.fields import RichTextField
from colorfield.fields import ColorField
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from django_extensions.db.fields import AutoSlugField
from jalali_date import date2jalali

from account_module.models import User


def my_slugify_function(content):
    return slugify(content, allow_unicode=True)


class Product(models.Model):
    title = models.CharField(max_length=300, unique=True, verbose_name='نام محصول')
    image = models.ImageField(upload_to='images/product', verbose_name='تصویر محصول')
    price = models.PositiveBigIntegerField(verbose_name='قیمت محصول')
    availability_count = models.PositiveIntegerField(null=True, blank=True, verbose_name='تعداد موجودی محصول',
                                                     help_text='- به غیر از محصولاتی که رنگ دارند')
    short_description = models.CharField(max_length=400, db_index=True, verbose_name='توضیحات کوتاه')
    description = RichTextField(verbose_name='توضیحات', db_index=True)
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد', editable=False)
    category = models.ManyToManyField('ProductCategory', verbose_name='دسته بندی')
    tag = models.ManyToManyField('ProductTag', verbose_name='تگ های محصول')
    grind = models.ManyToManyField('ProductGrind', null=True, blank=True, verbose_name='انتخاب دستگاه برای آسیاب')
    is_active = models.BooleanField(default=False, verbose_name='فعال / غیر فعال')
    status = models.BooleanField(default=True, verbose_name='موجود / ناموجود')
    slug = AutoSlugField(populate_from=['title'], unique=True, allow_unicode=True, slugify_function=my_slugify_function,
                         db_index=True, verbose_name='عنوان در url')

    def has_unavailable_colors(self):
        if self.productcolor_set.exists():
            return all(color.count == 0 for color in self.productcolor_set.all())
        elif self.status:
            return False
        return True

    def is_unavailable(self):
        return all(color.count == 0 for color in self.productcolor_set.all())

    def save(self, *args, **kwargs):
        if self.availability_count == 0:
            self.status = False
        else:
            self.status = True
        super(Product, self).save()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'
        ordering = ['-status', '-create_date']

    def get_jalali_create_date(self):
        return date2jalali(self.create_date)

    get_jalali_create_date.short_description = 'تاریخ ایجاد'

    def get_absolute_url(self):
        return reverse('product_detail', args=[self.slug])


class Coupon(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    used_by = models.ManyToManyField(User, blank=True, verbose_name='کاربر')
    code = models.CharField(max_length=6, unique=True, verbose_name='کد تخفیف')
    discount = models.PositiveIntegerField(verbose_name='درصد تخفیف')
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    is_active = models.BooleanField()

    def save(self, *args, **kwargs):
        now = timezone.now()
        if now > self.valid_to:
            self.is_active = False
        else:
            self.is_active = True
        super(Coupon, self).save()


class ProductGallery(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    image = models.ImageField(upload_to='images/product_gallery', verbose_name='تصویر')
    is_active = models.BooleanField(default=False, verbose_name='فعال / غیرفعال')

    def __str__(self):
        return self.product.title

    class Meta:
        verbose_name = 'گالری'
        verbose_name_plural = 'گالری تصاویر محصولات'


class ProductTag(models.Model):
    title = models.CharField(max_length=25, verbose_name='عنوان تگ')
    url_title = models.CharField(max_length=100, null=True, blank=True, verbose_name='عنوان تگ در url')
    is_active = models.BooleanField(default=False, verbose_name='فعال / غیرفعال')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'تگ محصول'
        verbose_name_plural = 'تگ های محصول'


class ProductColor(models.Model):
    title = models.CharField(max_length=20, verbose_name='نام رنگ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    count = models.PositiveIntegerField(verbose_name='تعداد رنگ موجود برای محصول')
    color = ColorField(default='#ffffff', verbose_name='رنگ محصول')
    status = models.BooleanField(default=True, verbose_name='موجود / ناموجود')
    is_active = models.BooleanField(default=False, verbose_name='فعال / غیرفعال')

    def save(self, *args, **kwargs):
        if self.count == 0:
            self.status = False
        else:
            self.status = True
        super(ProductColor, self).save()

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'رنگ محصول'
        verbose_name_plural = 'رنگ های محصولات'


class ProductCategory(models.Model):
    title = models.CharField(max_length=30, verbose_name='نام دسته بندی محصول')
    url_title = models.CharField(max_length=30, verbose_name='عنوان در url')
    is_active = models.BooleanField(default=False, verbose_name='فعال / غیرفعال')

    def __str__(self):
        return f"{self.title} - {self.url_title}"

    class Meta:
        verbose_name = 'دسته بندی محصولات'
        verbose_name_plural = 'دسته بندی های محصول'


class ProductGrind(models.Model):
    title = models.CharField(max_length=50, verbose_name='نام دستگاه آسیاب')
    is_active = models.BooleanField(default=False, verbose_name='فعال / غیرفعال')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'آسیاب محصول'
        verbose_name_plural = 'آسیاب های محصولات'
