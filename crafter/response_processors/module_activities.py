from crafter.models import CourseModuleLearningActivity, ModuleQuestion, ModuleResponseOption


def module_activities_postprocess(module, user, module_json):

    # remove existing activities for module
    CourseModuleLearningActivity.objects.filter(course_module=module).delete()
    ModuleQuestion.objects.filter(course_module=module).delete()

    for idxa, activity in enumerate(module_json['activities']):
        cma = CourseModuleLearningActivity()
        cma.course_module = module
        cma.title = activity['activity_title']
        cma.description = activity['activity_description']
        cma.order_by = idxa + 1
        cma.save()

    for idxq, question in enumerate(module_json['questions']):
        cmq = ModuleQuestion()
        cmq.course_module = module
        cmq.question = question['question_title']
        cmq.save()

        for idxr, response in enumerate(question['response_options']):
            cmr = ModuleResponseOption()
            cmr.module_question = cmq
            cmr.response = response['response_title']
            if response['correct_response']:
                cmr.score = 1
            cmr.save()

