from django.db.models import Count, Q
from django.http import HttpRequest
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from article_module.models import Article, ArticleCategory, ArticleTag, TopArticle


class ArticleListView(ListView):
    model = Article
    template_name = 'article_module/article_list.html'
    paginate_by = 6
    context_object_name = 'articles'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data()
        context['top_articles'] = TopArticle.objects.filter(is_active=True)[:3]
        return context

    def get_queryset(self):
        query = super(ArticleListView, self).get_queryset()
        query = query.filter(is_active=True)
        category_name = self.kwargs.get('cat')
        tag_name = self.kwargs.get('tag')
        if tag_name:
            query = query.filter(tag__url_title__iexact=tag_name)
        if category_name:
            query = query.filter(category__url_title__iexact=category_name)
        return query


class ArticleDetailView(DetailView):
    template_name = 'article_module/article_detail.html'
    model = Article

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data()
        loaded_article = self.object
        context['article_category'] = ArticleCategory.objects.filter(is_active=True, article=loaded_article.id).first()
        context['article_tags'] = ArticleTag.objects.filter(article=loaded_article.id, is_active=True)
        context['recent_articles'] = Article.objects.filter(is_active=True)[:3]
        return context

    def get(self, request: HttpRequest, *args, **kwargs):
        article = self.get_object()
        article.visit_count += 1
        article.save()
        return super().get(request, *args, **kwargs)


def article_category_component(request):
    article_categories = ArticleCategory.objects.annotate(
        article_counts=Count('article', filter=Q(article__is_active=True)))
    context = {
        'article_categories': article_categories
    }
    return render(request, 'article_module/component/article_category_component.html', context)
