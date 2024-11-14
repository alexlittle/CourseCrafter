from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

class Course(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    create_date = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=100, blank=False, null=False)

    def __str__(self):
        return self.title

def user_directory_path(instance, filename):
    return f"user_{instance.user.id}/course_{instance.course.id}/{filename}"

class CourseResource(models.Model):
    course = models.ForeignKey(Course, null=False, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    create_date = models.DateTimeField(default=timezone.now)
    url = models.CharField(max_length=300, blank=True, null=True, default=None)
    file = models.FileField(upload_to=user_directory_path)