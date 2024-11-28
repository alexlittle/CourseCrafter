from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


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


class CourseModuleLearningOutcome(models.Model):
    course_module = models.ForeignKey(CourseModule, null=True, related_name='coursemodulelos', on_delete=models.CASCADE)
    create_date = models.DateTimeField(default=timezone.now)
    learning_outcome = models.TextField(blank=True, null=True, default=None)
    order_by = models.IntegerField(default=0)


class CourseModuleLearningActivity(models.Model):
    course_module = models.ForeignKey(CourseModule, null=True, related_name='coursemodulelas', on_delete=models.CASCADE)
    create_date = models.DateTimeField(default=timezone.now)
    title = models.TextField(blank=True, null=True, default=None)
    description = models.TextField(blank=True, null=True, default=None)
    order_by = models.IntegerField(default=0)



