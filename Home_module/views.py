from django.db.models import Sum, Count, F
from django.shortcuts import render
from django.views.generic import TemplateView

from article_module.models import Article
from order_module.models import OrderDetail, Order
from product_module.models import Product
from site_module.models import SiteSetting, FooterLinkBox, SiteSettingCategory, TopProduct, SocialMedia


# Create your views here.

def home_page(request):
    articles = Article.objects.filter(is_active=True)[:3]
    site_setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
    site_setting_category = SiteSettingCategory.objects.filter(is_active=True)[:3]
    most_bought_product = Product.objects.filter(orderdetail__order__is_paid=True, is_active=True,
                                                 status=True).annotate(order_count=Sum('orderdetail__count')).order_by(
        '-order_count')[:4]
    top_products = TopProduct.objects.filter(is_active=True)[:6]

    if request.user.is_authenticated:
        orders = OrderDetail.objects.filter(order__is_paid=False, order__user=request.user).aggregate(
            total_count=Sum('count'))
    else:
        orders = 0

    context = {
        'articles': articles,
        'site_setting': site_setting,
        'site_setting_category': site_setting_category,
        'most_bought_product': most_bought_product,
        'top_products': top_products,
        'count': orders
    }
    return render(request, 'home_module/index.html', context)


def site_header_component(request):
    site_setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
    # basket = OrderDetail.objects.filter(order__user=request.user, order__is_paid=False).count()
    context = {
        'site_setting': site_setting,
    }
    return render(request, 'shared/site_header_component.html', context)


def site_footer_component(request):
    site_setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
    footer_box_link = FooterLinkBox.objects.all()
    social_media = SocialMedia.objects.filter(is_active=True).first()
    context = {
        'site_setting': site_setting,
        'footer_link_box': footer_box_link,
        'social_medias': social_media
    }
    return render(request, 'shared/site_footer_component.html', context)


class AboutView(TemplateView):
    template_name = 'home_module/about_us.html'

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data()
        context['site_setting'] = SiteSetting.objects.filter(is_main_setting=True).first()
        return context


def handler404(request, exception):
    return render(request, '404.html', status=404)
