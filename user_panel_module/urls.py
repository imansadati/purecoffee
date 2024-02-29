from django.urls import path

from . import views

urlpatterns = [
    path('basket/', views.user_basket, name='user_basket'),
    path('checkout/', views.CheckoutView.as_view(), name='user_checkout'),
    path('dashboard/', views.dashboard, name='user_dashboard'),
    path('change-order-detail', views.change_order_detail, name='change_order_detail'),
    path('remove-order-detail', views.remove_order_detail, name='remove_order_detail'),
    path('change-password', views.ChangePasswordUser.as_view(), name='user_change_password'),
    path('my-shopping', views.UserShopping.as_view(), name='user_shopping'),
    path('my-detail-shopping/<int:order_id>', views.user_detail_shopping, name='user_detail_shopping'),
]
