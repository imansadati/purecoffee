from django.db import transaction

from product_module.models import ProductColor


@transaction.atomic
def remove_unavailable_products_from_basket(order):
    # Iterate through order details
    for order_detail in order.orderdetail_set.all():
        if order_detail.color:
            # Check if the product color is available
            product_color = ProductColor.objects.get(title=order_detail.color, product__orderdetail=order_detail)
            if product_color.count <= 0:
                # Remove the order detail if the product color is unavailable
                order_detail.delete()
        else:
            # Check if the product is available
            if order_detail.product.availability_count <= 0:
                # Remove the order detail if the product is unavailable
                order_detail.delete()
