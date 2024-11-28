from django.contrib import admin
from crafter.models import Course, CourseResource, CourseVersion, CourseVersionLearningOutcome, CourseModule, \
    CourseModuleLearningOutcome, CourseModuleLearningActivity


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('shortname', 'title', 'create_date')


@admin.register(CourseResource)
class CourseResourceAdmin(admin.ModelAdmin):
    list_display = ('course', 'url', 'file')


@admin.register(CourseVersion)
class CourseVersionAdmin(admin.ModelAdmin):
    list_display = ('course', 'title', 'version_number', 'create_date', 'description')


@admin.register(CourseVersionLearningOutcome)
class CourseVersionLearningOutcomeAdmin(admin.ModelAdmin):
    list_display = ('course_version', 'create_date', 'learning_outcome', 'order_by')


@admin.register(CourseModule)
class CourseModuleAdmin(admin.ModelAdmin):
    list_display = ('course_version', 'title', 'description', 'order_by')


@admin.register(CourseModuleLearningOutcome)
class CourseModuleLearningOutcomeAdmin(admin.ModelAdmin):
    list_display = ('course_module', 'create_date', 'learning_outcome', 'order_by')


@admin.register(CourseModuleLearningActivity)
class CourseModuleLearningActivityAdmin(admin.ModelAdmin):
    list_display = ('course_module', 'title', 'description', 'order_by')