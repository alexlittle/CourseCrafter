from pprint import pprint

from django.core.management.base import BaseCommand
from django.utils.translation import gettext_lazy as _

from crafter.coursecrafterai import CourseCrafterAI

class Command(BaseCommand):
    help = _(u"For testing the assistant via the command line")
    errors = []

    def handle(self, *args, **options):


        urls = [
            'https://en.wikipedia.org/wiki/Winchester',
            'https://en.wikipedia.org/wiki/Winchester_Cathedral',
            'https://en.wikipedia.org/wiki/Winchester_Castle'
        ]
        course_id="his-win3"
        course_title = "History of Winchester"
        ccai = CourseCrafterAI(course_id)

        vs = ccai.get_vs()

        vs.reset_collection()
    
        for url in urls:
            print(f"loading {url}")

            result, splits = ccai.load_url(url)
            if result:
                vs.add_documents(splits)
                print(f"added {url}")

        ccai.init_chat()
        response = ccai.query(course_title, 'course_outline')
        pprint(response)
