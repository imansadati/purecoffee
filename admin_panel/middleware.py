from django.http import HttpRequest, HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse


class AdminPanelMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request: HttpRequest):
        if request.path.startswith('/admin-panel/') and request.path != reverse(
                'login_user_admin_page') and not request.user.is_staff:
            return HttpResponseRedirect(reverse('login_user_admin_page'))
        return self.get_response(request)
