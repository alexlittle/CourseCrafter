from django.contrib import admin
from crafter.models import Course, CourseResource


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'create_date')

@admin.register(CourseResource)
class CourseResourceAdmin(admin.ModelAdmin):
    list_display = ('course', 'url', 'file')