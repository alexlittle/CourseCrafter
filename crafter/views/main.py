from django.views.generic import TemplateView
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy
from django.conf import settings

from crafter.models import Course


class HomeView(TemplateView):
    template_name = 'crafter/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['courses'] = Course.objects.filter(user=self.request.user)

        context['model'] = f"{settings.CRAFTER_CHAT_ENGINE} ({settings.CRAFTER_CHAT_ENGINE_MODEL})"
        return context

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('crafter:index')