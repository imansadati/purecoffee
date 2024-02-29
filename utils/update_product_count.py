from django.db import transaction

from product_module.models import ProductColor


@transaction.atomic
def update_product_counts(order):
    # Iterate through order details
    for order_detail in order.orderdetail_set.all():
        # Check if the order detail has a color
        if order_detail.color:
            # Update the count for the specific product color
            product_color = ProductColor.objects.get(title=order_detail.color, product__orderdetail=order_detail)
            product_color.count -= order_detail.count
            product_color.save()
        else:
            # Update the count for the product (assuming there is a ForeignKey relationship)
            order_detail.product.availability_count -= order_detail.count
            order_detail.product.save()
