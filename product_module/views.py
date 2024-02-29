from django.db.models import Q, Count
from django.shortcuts import render
from django.views.generic import ListView, DetailView

from product_module.models import Product, ProductGallery, ProductTag, ProductColor, ProductCategory, ProductGrind
from site_module.models import SiteBanner, SocialMedia, TopProduct


class ProductListView(ListView):
    template_name = 'product_module/product_list.html'
    model = Product
    context_object_name = 'products'
    paginate_by = 6

    # ordering = '-status'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ProductListView, self).get_context_data()
        context['banners'] = SiteBanner.objects.filter(is_active=True)
        context['social_medias'] = SocialMedia.objects.filter(is_active=True).first()
        context['top_products'] = TopProduct.objects.filter(is_active=True)[:3]
        return context

    def get_queryset(self):
        query = super(ProductListView, self).get_queryset()
        query = query.filter(is_active=True)
        search_name = self.request.GET.get('search')
        category_name = self.kwargs.get('cat')
        tag_name = self.kwargs.get('tag')
        if tag_name is not None:
            query = query.filter(tag__url_title__iexact=tag_name)
            return query
        if category_name is not None:
            query = query.filter(category__url_title__iexact=category_name)
            return query
        lookup = Q(title__icontains=search_name) | Q(description__icontains=search_name) | Q(
            tag__title__icontains=search_name)
        if search_name:
            products = Product.objects.filter(lookup, is_active=True).distinct()
            return products
        else:
            return query.order_by('-status')


class ProductDetailView(DetailView):
    template_name = 'product_module/product_detail.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        loaded_product = self.object
        context['product_gallery'] = ProductGallery.objects.filter(product_id=loaded_product.id, is_active=True)
        context['product_tags'] = ProductTag.objects.filter(product=loaded_product.id, is_active=True)
        context['product_colors'] = ProductColor.objects.filter(product=loaded_product.id, status=True, is_active=True,
                                                                count__gte=1)
        context['product_categories'] = ProductCategory.objects.filter(product=loaded_product.id,
                                                                       is_active=True).first()
        context['product_grinds'] = ProductGrind.objects.filter(product=loaded_product.id, is_active=True)
        context['related_products'] = Product.objects.filter(category__product=loaded_product.id,
                                                             is_active=True).exclude(pk=loaded_product.id).distinct()
        context['social_medias'] = SocialMedia.objects.filter(is_active=True).first()
        context['top_products'] = TopProduct.objects.filter(is_active=True)[:3]
        return context


def product_category_component(request):
    product_category = ProductCategory.objects.annotate(
        products_count=Count('product', Q(product__is_active=True)))
    context = {
        'product_categories': product_category
    }
    return render(request, 'product_module/component/product_category_component.html', context)
