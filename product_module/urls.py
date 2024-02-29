from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.ProductListView.as_view(), name='product_list'),
    path('cat/<cat>', views.ProductListView.as_view(), name='product_category_list'),
    path('tag/<tag>', views.ProductListView.as_view(), name='product_tag_list'),
    re_path('(?P<slug>[-\w]+)/', views.ProductDetailView.as_view(), name='product_detail'),
]
