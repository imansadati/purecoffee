from django.urls import path
from . import views
from order_module.views import add_product_to_order

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('about-us', views.AboutView.as_view(), name='about_page'),
]
