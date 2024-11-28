import json

from celery import shared_task
from celery_progress.backend import ProgressRecorder

from django.contrib.auth.models import User
from django.urls import reverse

from crafter.models import Course, CourseResource, CourseModule, CourseModuleLearningOutcome
from crafter.coursecrafterai import CourseCrafterAI
from crafter.response_processors.course_outline import course_outline_postprocess
from crafter.response_processors.module_activities import module_activities_postprocess


# Celery Task
@shared_task(bind=True)
def generate_course(self, course_id, user_id):
	print('Task started')

	user = User.objects.get(pk=user_id)
	# Create the progress recorder instance to update the web page
	progress_recorder = ProgressRecorder(self)

	course = Course.objects.get(pk=course_id)
	course_resources = CourseResource.objects.filter(course=course)
	total = course_resources.count() + 4

	progress_recorder.set_progress(1, total, description="Loading CrafterAI")
	ccai = CourseCrafterAI(course.shortname)
	vs = ccai.get_vs()
	vs.reset_collection()
	progress_recorder.set_progress(2, total, description="Setting up vector store for urls")
	for idx, cr in enumerate(course_resources):
		result, splits = ccai.load_url(cr.url)
		if result:
			vs.add_documents(splits)
			progress_recorder.set_progress(idx + 3, total, description=f"Added {cr.url}")
	progress_recorder.set_progress(total-1, total, description="generating CrafterAI response")
	ccai.init_chat()
	response = ccai.query(course.title)

	course_version = course_outline_postprocess(course, user, response)

	course_modules = CourseModule.objects.filter(course_version=course_version)
	for module in course_modules:
		los = CourseModuleLearningOutcome.objects.filter(course_module=module)
		learning_outcomes = "\n".join(lo.learning_outcome for lo in los)
		response = ccai.create_module_activities(module.title, learning_outcomes)

		module_activities_postprocess(module, user, response)

	progress_recorder.set_progress(total, total, description="complete")

	return "Your course has been created. <a href='{}'>View your course</a>".format(reverse('crafter:versionview', kwargs={'id': course_version.id }))