from django.views.generic import TemplateView


class HomeView(TemplateView):
    template_name = 'crafter/home.html'

