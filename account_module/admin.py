from django.contrib import admin

from account_module.models import User


# Register your models here.


class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_active']


admin.site.register(User, UserAdmin)
