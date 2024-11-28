import json

from celery import shared_task
from celery_progress.backend import ProgressRecorder
from django.contrib.auth.models import User
from crafter.models import Course, CourseResource, CourseVersion, CourseModule, CourseModuleLearningOutcome
from crafter.coursecrafterai import CourseCrafterAI

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
	progress_recorder.set_progress(total, total, description="processing response")

	print(response)

	course_json = response
	# course version
	course_version = CourseVersion()
	course_version.user = user
	course_version.course = course
	course_version.title = course_json['title']
	course_version.save()

	# course modules
	for idxm, module in enumerate(course_json['modules']):
		course_module = CourseModule()
		course_module.course_version = course_version
		course_module.title = module['module_title']
		course_module.order_by = idxm+1
		course_module.save()

		# course modules LOs
		for idxl, lo in enumerate(module['learning_outcomes']):
			cmlo = CourseModuleLearningOutcome()
			cmlo.course_module = course_module
			cmlo.learning_outcome = lo['title']
			cmlo.order_by = idxl +1
			cmlo.save()

	return response