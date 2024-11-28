from django.views.generic import TemplateView, FormView
from crafter.forms import CourseLinkFormSet, CourseForm
from django.shortcuts import redirect
from django.urls import reverse
from django.shortcuts import render
from crafter.models import Course, CourseResource
from crafter.asynctasks.generate_course import generate_course



class SetupCourseView(FormView):
    template_name = 'crafter/setup.html'
    form_class = CourseLinkFormSet

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if 'courseform' not in context:
            context['courseform'] = CourseForm()
        if 'formset' not in context:
            context['formset'] = CourseLinkFormSet()
        return context

    def post(self, request, *args, **kwargs):
        formset = CourseLinkFormSet(request.POST)
        courseform = CourseForm(request.POST)
        if courseform.is_valid() and formset.is_valid():
            # Handle valid data
            urls = [form.cleaned_data['url'] for form in formset if form.cleaned_data.get('url')]
            course = Course()
            course.user = request.user
            course.shortname = courseform.cleaned_data.get('shortname')
            course.title = courseform.cleaned_data.get('title')
            course.save()
            for url in urls:
                cr = CourseResource()
                cr.course = course
                cr.user = request.user
                cr.url = url
                cr.save()
        return redirect(reverse('crafter:generate', args=[course.id]))

class GenerateCourseView(TemplateView):
    template_name = 'crafter/generate.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        course = Course.objects.get(pk=self.kwargs.get('id'))
        context['course'] = course
        context['courseresources'] = CourseResource.objects.filter(course=course)
        return context

    def post(self, request, *args, **kwargs):
        # Create Task
        gen_task = generate_course.delay(self.kwargs.get('id'), request.user.id)
        # Get ID
        task_id = gen_task.task_id
        # Print Task ID
        print(f'Celery Task ID: {task_id}')
        # Return demo view with Task ID
        context = self.get_context_data(**kwargs)
        context['task_id'] = task_id
        return render(request, 'crafter/progress.html', context)