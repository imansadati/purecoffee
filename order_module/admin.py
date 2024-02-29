from django.contrib import admin

from order_module.models import Order, OrderDetail, Wholesale


# Register your models here.

class OrderAdmin(admin.ModelAdmin):
    list_display = ['user', 'is_paid']


class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ['product', 'count', 'final_price']


admin.site.register(Order, OrderAdmin)
admin.site.register(Wholesale)
admin.site.register(OrderDetail, OrderDetailAdmin)
