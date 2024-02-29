from django.contrib import admin

from contact_module.models import ContactUs


# Register your models here.


class ContactUsAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'title', 'get_jalali_create_date', 'is_read_by_admin']


admin.site.register(ContactUs, ContactUsAdmin)
