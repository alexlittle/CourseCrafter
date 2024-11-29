from pprint import pprint

from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _

from crafter.coursecrafterai import CourseCrafterAI
from crafter.models import CourseModuleLearningOutcome, CourseVersion, ModuleQuestion
from crafter.response_processors.skill_sets import skillset_postprocess


class Command(BaseCommand):
    help = _(u"For testing the assistant via the command line")
    errors = []

    def handle(self, *args, **options):

        course_version = CourseVersion.objects.get(pk=19)

        # all learning outcomes to string
        los = CourseModuleLearningOutcome.objects.filter(course_module__course_version=course_version)
        learning_outcomes = "\n".join(f"{lo.learning_outcome} (id: {lo.id})" for lo in los)

        # all questions to string
        qs = ModuleQuestion.objects.filter(course_module__course_version=course_version)
        questions = "\n".join(f"{q.question} (id: {q.id})" for q in qs)


        ccai = CourseCrafterAI(course_version.course.shortname)
        ccai.init_chat()
        response = ccai.create_skill_sets(learning_outcomes, questions)
        pprint(response)


        skillset_postprocess(course_version, response)