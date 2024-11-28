import random

from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

from crafter.models import CourseVersion, ModuleQuestion
from crafter.forms import QuizForm

class CourseVersionView(LoginRequiredMixin, TemplateView):
    template_name = 'crafter/version_view.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['version'] = CourseVersion.objects.get(pk=self.kwargs.get('id'), course__user=self.request.user)
        return context


class PreTestView(LoginRequiredMixin, TemplateView):
    template_name = 'crafter/run/pre_test.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_version = CourseVersion.objects.get(pk=self.kwargs.get('id'))
        context['course'] = course_version

        ids = ModuleQuestion.objects.filter(course_module__course_version=course_version).values_list('id', flat=True)

        # Randomly select 5 IDs
        random_ids = random.sample(list(ids), 5)

        # Retrieve the corresponding records
        questions = ModuleQuestion.objects.filter(id__in=random_ids)

        form = QuizForm(questions=questions)
        context['form'] = form
        return context