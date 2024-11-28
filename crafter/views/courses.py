from django.views.generic import TemplateView

from crafter.models import CourseVersion




class CourseVersionView(TemplateView):
    template_name = 'crafter/version_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['version'] = CourseVersion.objects.get(pk=self.kwargs.get('id'), course__user=self.request.user)
        return context