from django.contrib import admin

from site_module.models import SiteSetting, FooterLinkBox, FooterLink, SiteBanner, SiteSettingCategory, TopProduct, \
    SocialMedia


# Register your models here.


class FooterLinkAdmin(admin.ModelAdmin):
    list_display = ['title', 'url', 'footer_link_box']


class SiteBannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'position', 'is_active']


class SocialMediaAdmin(admin.ModelAdmin):
    list_display = ['instagram', 'telegram', 'whatsapp', 'youtube']


class TopProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active']
    list_editable = ['is_active']


admin.site.register(SiteSetting)
admin.site.register(FooterLink, FooterLinkAdmin)
admin.site.register(FooterLinkBox)
admin.site.register(SiteSettingCategory)
admin.site.register(SocialMedia, SocialMediaAdmin)
admin.site.register(TopProduct, TopProductAdmin)
admin.site.register(SiteBanner, SiteBannerAdmin)
