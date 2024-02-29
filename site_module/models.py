from django.db import models

from article_module.models import Article
from product_module.models import ProductCategory, Product


class SiteSetting(models.Model):
    site_name = models.CharField(max_length=30, verbose_name='نام سایت')
    site_name_title = models.CharField(max_length=150, verbose_name='نام سایت در گوگل')
    site_description = models.TextField(verbose_name='درباره سایت')
    short_description = models.CharField(max_length=150, verbose_name='توضیحات کوتاه سایت')
    products_count = models.IntegerField(verbose_name='تعداد محصولات')
    customer_count = models.IntegerField(verbose_name='تعداد مشتریان')
    phone_number = models.IntegerField(verbose_name='شماره تماس سایت')
    email = models.EmailField(verbose_name='آدرس ایمیل')
    site_icon_circle = models.ImageField(upload_to='images/site_setting', null=True, blank=True,
                                         verbose_name='لوگوی دایره ای سایت')
    site_icon = models.ImageField(upload_to='images/site_setting', verbose_name='لوگو کوچک سایت')
    about_us_image = models.ImageField(upload_to='images/site_setting', verbose_name='تصویر صفحه درباره ما')
    copyright = models.CharField(max_length=150, verbose_name='متن کپی رایت')
    newletter_text = models.CharField(max_length=200, verbose_name='متن خبر نامه سایت')
    why_pure_text = models.TextField(verbose_name='متن چرا ما را باید انتخاب کنید')
    shipping_amount = models.IntegerField(default=0, verbose_name='هزینه حمل و نقل')
    is_main_setting = models.BooleanField(default=True, verbose_name='تنظیم به عنوان تنظیمات اصلی')

    def __str__(self):
        return self.site_name

    class Meta:
        verbose_name = 'تنظیمات سایت'
        verbose_name_plural = 'تنظیمات سایت'


class FooterLinkBox(models.Model):
    title = models.CharField(max_length=150, verbose_name='عنوان')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی لینک های فوتر'
        verbose_name_plural = 'دسته بندی های لینک های فوتر'


class FooterLink(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    url = models.URLField(max_length=600, verbose_name='لینک')
    footer_link_box = models.ForeignKey(FooterLinkBox, on_delete=models.CASCADE, verbose_name='دسته بندی')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'لینک فوتر'
        verbose_name_plural = 'لینک های فوتر'


class SiteBanner(models.Model):
    class SiteBannerPosition(models.TextChoices):
        product_list = 'product_list', 'صفحه لیست محصولات'
        product_detail = 'product_detail', 'صفحه جزییات محصولات'

    title = models.CharField(max_length=80, verbose_name='عنوان بنر')
    url = models.URLField(max_length=500, verbose_name='آدرس ulr بنر')
    image = models.ImageField(upload_to='images/banners', verbose_name='تصویر بنر')
    is_active = models.BooleanField(default=False, verbose_name='فعال / غیرفعال')
    position = models.CharField(max_length=200, choices=SiteBannerPosition.choices,
                                verbose_name='محل قرار گیری بنر در سایت')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'بنر تبلیغاتی'
        verbose_name_plural = 'بنر های تبلیغاتی'


class SiteSettingCategory(models.Model):
    title = models.CharField(max_length=50, verbose_name='عنوان')
    short_description = models.CharField(max_length=300, verbose_name='توضیحات کوتاه')
    image = models.ImageField(upload_to='images/site_setting', verbose_name='تصویر')
    product_category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name='دسته بندی محصول')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی محصول در سایت'
        verbose_name_plural = 'دسته بندی های محصول در سایت'


class TopProduct(models.Model):
    title = models.CharField(max_length=100, verbose_name='نام محصول')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='محصول')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'محصول برتر'
        verbose_name_plural = 'محصولات برتر'


class SocialMedia(models.Model):
    instagram = models.CharField(max_length=50, null=True, blank=True, verbose_name='آیدی اینستاگرام')
    telegram = models.CharField(max_length=50, null=True, blank=True, verbose_name='آیدی تلگرام')
    whatsapp = models.CharField(max_length=50, null=True, blank=True, verbose_name='آیدی واتساپ')
    youtube = models.CharField(max_length=130, null=True, blank=True, verbose_name='آدرس یوتیوب')
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'شبکه اجتماعی'
        verbose_name_plural = 'شبکه های اجتماعی'
