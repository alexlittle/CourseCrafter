import json

from crafter.models import CourseModuleLearningOutcome, ModuleQuestion, Skill, LearningOutcomeSkill, QuestionSkill

test_json = """{"skillsets": [{"learning_outcome_ids": [236, 237, 239, 240],
                "question_ids": [61, 64, 65, 69, 70],
                "skill_shortname": "roman-early-medieval",
                "skill_title": "Understanding Winchesters Roman and Early Medieval History"},
               {"learning_outcome_ids": [238, 242, 254],
                "question_ids": [63, 66, 82],
                "skill_shortname": "physical-governance",
                "skill_title": "Analyzing Winchesters Physical Development and Governance"},
               {"learning_outcome_ids": [241, 247, 248, 252, 256],
                "question_ids": [67, 68, 71, 78, 84],
                "skill_shortname": "religious-cultural",
                "skill_title": "Evaluating Winchesters Religious and Cultural Significance"},
               {"learning_outcome_ids": [244, 245, 246],
                "question_ids": [72, 73, 74, 75, 76],
                "skill_shortname": "architectural-heritage",
                "skill_title": "Assessing Winchesters Architectural Heritage"},
               {"learning_outcome_ids": [249, 250, 251, 253],
                "question_ids": [77, 79, 80, 81],
                "skill_shortname": "post-medieval",
                "skill_title": "Tracing Winchesters Post-Medieval Development"},
               {"learning_outcome_ids": [254, 255, 257, 258],
                "question_ids": [82, 83, 85, 86],
                "skill_shortname": "modern-winchester",
                "skill_title": "Exploring Winchesters Modern Identity and Institutions"},
               {"learning_outcome_ids": [234, 235, 237],
                "question_ids": [62, 69],
                "skill_shortname": "prehistoric-roman",
                "skill_title": "Interpreting Archaeological Evidence of Prehistoric and Roman Winchester"}]}"""


def skillset_validate(course_version, skillset_json):
    # get all the learning outcomes in course
    los = CourseModuleLearningOutcome.objects.filter(
        course_module__course_version=course_version).values_list('id', flat=True)

    skill_json_ids = []
    for skill in skillset_json['skillsets']:
        skill_json_ids.extend(skill['learning_outcome_ids'])
    print(len(list(set(skill_json_ids))))
    print(len(los))

    missing_from_json =  list(set(los) - set(skill_json_ids))
    print(missing_from_json)

    qs = ModuleQuestion.objects.filter(course_module__course_version=course_version).values_list('id', flat=True)

    q_json_ids = []
    for skill in skillset_json['skillsets']:
        q_json_ids.extend(skill['question_ids'])
    print(len(list(set(q_json_ids))))
    print(len(qs))

    missing_from_json = list(set(qs) - set(q_json_ids))
    print(missing_from_json)

def skillset_postprocess(course_version, skillset_json):
    skillset_validate(course_version, skillset_json)

    # remove existing LO Skills
    LearningOutcomeSkill.objects.filter(learning_outcome__course_module__course_version=course_version).delete()

    # remove existing Question Skills
    QuestionSkill.objects.filter(question__course_module__course_version=course_version).delete()

    # add to db
    for skill_json in skillset_json['skillsets']:
        # get or create the skill
        skill, created = Skill.objects.get_or_create(
            shortname=skill_json['skill_shortname'],
            defaults={'description': skill_json['skill_title']}
        )

        # add to each LO
        for lo_id in skill_json['learning_outcome_ids']:
            lo = CourseModuleLearningOutcome.objects.get(pk=lo_id)
            LearningOutcomeSkill.objects.get_or_create(
                learning_outcome=lo,
                skill=skill
            )

        # add to each question
        for q_id in skill_json['question_ids']:
            q = ModuleQuestion.objects.get(pk=q_id)
            QuestionSkill.objects.get_or_create(
                question=q,
                skill=skill
            )


