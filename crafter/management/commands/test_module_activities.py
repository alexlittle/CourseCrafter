from pprint import pprint

from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _

from crafter.coursecrafterai import CourseCrafterAI
from crafter.models import CourseModule, CourseModuleLearningOutcome
from crafter.response_processors.module_activities import module_activities_postprocess


class Command(BaseCommand):
    help = _(u"For testing the assistant via the command line")
    errors = []

    def handle(self, *args, **options):

        module_ids = [52, 53, 54]



        for module_id in module_ids:
            module = CourseModule.objects.get(pk=module_id)

            los = CourseModuleLearningOutcome.objects.filter(course_module=module)
            learning_outcomes = "\n".join(lo.learning_outcome for lo in los)
            ccai = CourseCrafterAI(module.course_version.course.shortname)
            ccai.init_chat()
            response = ccai.create_module_activities(module.title, learning_outcomes)
            pprint(response)

            module_activities_postprocess(module, 1, response)

