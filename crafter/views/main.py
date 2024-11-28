from django.views.generic import TemplateView
from crafter.models import Course
from django.contrib.auth.views import LogoutView
from django.urls import reverse_lazy

class HomeView(TemplateView):
    template_name = 'crafter/home.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['courses'] = Course.objects.filter(user=self.request.user)
        return context

class UserLogoutView(LogoutView):
    next_page = reverse_lazy('crafter:index')