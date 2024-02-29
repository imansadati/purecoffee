from django.shortcuts import render
from django.views.generic.edit import CreateView

from contact_module.forms import ContactUsModelForm
from site_module.models import SiteSetting, SocialMedia


# Create your views here.


class ContactUsView(CreateView):
    form_class = ContactUsModelForm
    template_name = 'contact_module/contact_us.html'
    success_url = '/contact-us/'

    def get_context_data(self, **kwargs):
        context = super(ContactUsView, self).get_context_data()
        context['site_setting'] = SiteSetting.objects.filter(is_main_setting=True).first()
        context['social_medias'] = SocialMedia.objects.filter(is_active=True).first()
        return context
