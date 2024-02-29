from ckeditor.fields import RichTextField
from django.db import models
from django.urls import reverse
from jalali_date import date2jalali


class Article(models.Model):
    title = models.CharField(max_length=230, verbose_name='عنوان')
    short_description = models.TextField(verbose_name='توضیحات کوتاه')
    description = RichTextField(verbose_name='توضیحات', db_index=True)
    slug = models.SlugField(max_length=50, allow_unicode=True, db_index=True, verbose_name='عنوان در url')
    category = models.ManyToManyField('ArticleCategory', verbose_name='دسته بندی مقاله')
    tag = models.ManyToManyField('ArticleTag', verbose_name='تگ مقاله')
    image = models.ImageField(upload_to='images/article', verbose_name='تصویر')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد', editable=False)
    visit_count = models.IntegerField(default=0, verbose_name='تعداد بازدید')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'
        ordering = ['-create_date']

    def __str__(self):
        return self.title

    def get_jalali_create_date(self):
        return date2jalali(self.create_date)

    get_jalali_create_date.short_description = 'تاریخ ایجاد'

    def get_absolute_url(self):
        return reverse('article_detail_page', args=[self.slug])


class ArticleCategory(models.Model):
    title = models.CharField(max_length=50, verbose_name='عنوان')
    url_title = models.CharField(unique=True, max_length=100, verbose_name='عنوان در url')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی مقاله'
        verbose_name_plural = 'دسته بندی های مقاله'


class ArticleTag(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    url_title = models.CharField(max_length=200, verbose_name='عنوان در url')
    is_active = models.BooleanField(default=True, verbose_name='فعال / ؛یرفعال')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'تگ مقاله'
        verbose_name_plural = 'تگ های مقالات'


class TopArticle(models.Model):
    title = models.CharField(max_length=150, verbose_name='عنوان')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='مقاله')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیرفعال')
    short_description = models.CharField(max_length=120, verbose_name='توضیحات کوتاه')
