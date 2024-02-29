from django.urls import path, re_path

from article_module.views import ArticleListView, ArticleDetailView

urlpatterns = [
    path('', ArticleListView.as_view(), name='article_list_page'),
    path('cat/<cat>', ArticleListView.as_view(), name='article_category_page'),
    path('tag/<tag>', ArticleListView.as_view(), name='article_tag_page'),
    re_path('(?P<slug>[-\w]+)/', ArticleDetailView.as_view(), name='article_detail_page'),
]
