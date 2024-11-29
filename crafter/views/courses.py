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

    def generate_questions(self, course_version, num_questions=5):
        ids = list(ModuleQuestion.objects.filter(course_module__course_version=course_version).values_list('id', flat=True))
        random_ids = random.sample(list(ids), min(num_questions, len(ids)))
        questions = ModuleQuestion.objects.filter(id__in=random_ids)
        return questions

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course_version = CourseVersion.objects.get(pk=self.kwargs.get('id'))
        context['course'] = course_version
        session_cv_questions = 'quiz_questions_' + str(course_version.id)
        if session_cv_questions not in self.request.session:
            # Fetch new questions and save their IDs in the session
            questions = self.generate_questions(course_version.id, num_questions=5)
            self.request.session[session_cv_questions] = list(questions.values_list('id', flat=True))
        else:
            # Retrieve the same questions from the session
            question_ids = self.request.session[session_cv_questions]
            questions = ModuleQuestion.objects.filter(id__in=question_ids)

        form = QuizForm(questions=questions)
        context['form'] = form
        return context