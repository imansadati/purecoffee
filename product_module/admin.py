from django.contrib import admin

from product_module.models import *


class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'get_jalali_create_date', 'slug', 'availability_count', 'is_active']
    list_editable = ['is_active', 'price']


class ProductTagAdmin(admin.ModelAdmin):
    list_display = ['title', 'url_title', 'is_active']
    list_editable = ['is_active']


class ProductColorAdmin(admin.ModelAdmin):
    list_display = ['title', 'product', 'count', 'is_active']
    list_editable = ['is_active']


class ProductGalleryAdmin(admin.ModelAdmin):
    list_display = ['product', 'is_active']
    list_editable = ['is_active']


admin.site.register(Product, ProductAdmin)
admin.site.register(ProductCategory)
admin.site.register(Coupon)
admin.site.register(ProductGrind)
admin.site.register(ProductGallery, ProductGalleryAdmin)
admin.site.register(ProductColor, ProductColorAdmin)
admin.site.register(ProductTag, ProductTagAdmin)
