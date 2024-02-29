from django.contrib import admin

from article_module.models import Article, ArticleCategory, ArticleTag, TopArticle


class ArticleAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'get_jalali_create_date', 'is_active']
    list_editable = ['slug', 'is_active']


admin.site.register(Article, ArticleAdmin)
admin.site.register(ArticleCategory)
admin.site.register(TopArticle)
admin.site.register(ArticleTag)
