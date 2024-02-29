from django.http import HttpRequest, Http404

from order_module.models import Order


def check_basket_empty(view_func):
    def wrapper(request: HttpRequest, *args, **kwargs):
        basket = Order.objects.filter(user=request.user, is_paid=False).first()

        if not basket or basket.orderdetail_set.count() == 0:
            raise Http404('basket is empty')

        return view_func(request, *args, **kwargs)

    return wrapper
