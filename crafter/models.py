from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.db.models import Q

class Course(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    create_date = models.DateTimeField(default=timezone.now)
    shortname = models.CharField(max_length=20, blank=False, null=False, default=None)
    title = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.shortname + ' - ' + self.title

    class Meta:
        unique_together = ('user', 'shortname')


def user_directory_path(instance, filename):
    return f"user_{instance.user.id}/course_{instance.course.id}/{filename}"


class CourseResource(models.Model):
    course = models.ForeignKey(Course, null=False, related_name='courseresources', on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    create_date = models.DateTimeField(default=timezone.now)
    url = models.CharField(max_length=300, blank=True, null=True, default=None)
    file = models.FileField(upload_to=user_directory_path, blank=True, null=True, default=None)


class CourseVersion(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, null=False, related_name='courseversions', on_delete=models.CASCADE)
    create_date = models.DateTimeField(default=timezone.now)
    version_number = models.IntegerField(default=1)
    title = models.CharField(max_length=100, blank=True, null=True, default=None)
    description = models.TextField(blank=True, null=True, default=None)
    prompt_used = models.TextField(blank=True, null=True, default=None)

    def __str__(self):
        return self.title + f"({self.version_number})"

    def save(self, *args, **kwargs):
        if self.pk is None:
            latest_version = CourseVersion.objects.filter(course=self.course).order_by('-version_number').first()
            self.version_number = latest_version.version_number + 1 if latest_version else 1
        super().save(*args, **kwargs)


class CourseVersionLearningOutcome(models.Model):
    course_version = models.ForeignKey(CourseVersion, null=True, related_name='courseversionlos', on_delete=models.CASCADE)
    create_date = models.DateTimeField(default=timezone.now)
    learning_outcome = models.TextField(blank=True, null=True, default=None)
    order_by = models.IntegerField(default=0)


class CourseModule(models.Model):
    course_version = models.ForeignKey(CourseVersion, null=True, related_name='coursemodules', on_delete=models.CASCADE)
    title = models.TextField(blank=True, null=True, default=None)
    description = models.TextField(blank=True, null=True, default=None)
    order_by = models.IntegerField(default=0)

    def get_skills(self):
        skills = Skill.objects.filter(Q(loskill_skill__learning_outcome__course_module=self) |
                                      Q(questionskill_skill__question__course_module=self)).distinct()
        return skills

class CourseModuleLearningOutcome(models.Model):
    course_module = models.ForeignKey(CourseModule, null=True, related_name='coursemodulelos', on_delete=models.CASCADE)
    create_date = models.DateTimeField(default=timezone.now)
    learning_outcome = models.TextField(blank=True, null=True, default=None)
    order_by = models.IntegerField(default=0)

    def __str__(self):
        return self.learning_outcome

class CourseModuleLearningActivity(models.Model):
    course_module = models.ForeignKey(CourseModule, null=True, related_name='coursemodulelas', on_delete=models.CASCADE)
    create_date = models.DateTimeField(default=timezone.now)
    title = models.TextField(blank=True, null=True, default=None)
    description = models.TextField(blank=True, null=True, default=None)
    order_by = models.IntegerField(default=0)


class ModuleQuestion(models.Model):
    course_module = models.ForeignKey(CourseModule, related_name='modulequestions', on_delete=models.CASCADE)
    question = models.TextField(blank=False, null=False)

    def __str__(self):
        return self.question

class ModuleResponseOption(models.Model):
    module_question = models.ForeignKey(ModuleQuestion, related_name='questionresponses', on_delete=models.CASCADE)
    response = models.TextField(blank=False, null=False)
    score = models.IntegerField(default=0)

    def __str__(self):
        return self.response

class Skill(models.Model):
    shortname = models.CharField(max_length=100, blank=False, null=False, unique=True)
    description = models.TextField(blank=False, null=False)

    def __str__(self):
        return self.shortname

class LearningOutcomeSkill(models.Model):
    learning_outcome = models.ForeignKey(CourseModuleLearningOutcome, related_name='loskill_lo', on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, related_name='loskill_skill', on_delete=models.CASCADE)


class QuestionSkill(models.Model):
    question = models.ForeignKey(ModuleQuestion, related_name='questionskill_question', on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, related_name='questionskill_skill', on_delete=models.CASCADE)


