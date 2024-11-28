from crafter.models import CourseVersion, CourseModule, CourseModuleLearningOutcome

def course_outline_postprocess(course, user, course_json):

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
			cmlo.order_by = idxl + 1
			cmlo.save()

	return course_version
