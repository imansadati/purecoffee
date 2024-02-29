from django.shortcuts import redirect
from django.urls import reverse_lazy


class UnauthenticatedRequiredMixin:
    login_url = reverse_lazy('home_page')

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.login_url)
        else:
            pass
        return super().dispatch(request, *args, **kwargs)
