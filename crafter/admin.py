from django.contrib import admin
from crafter.models import Course, CourseResource, CourseVersion, CourseVersionLearningOutcome, CourseModule, \
    CourseModuleLearningOutcome, CourseModuleLearningActivity, ModuleQuestion, ModuleResponseOption, Skill, \
    LearningOutcomeSkill, QuestionSkill


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

@admin.register(ModuleQuestion)
class ModuleQuestionAdmin(admin.ModelAdmin):
    list_display = ('course_module', 'question')

@admin.register(ModuleResponseOption)
class ModuleResponseOptionAdmin(admin.ModelAdmin):
    list_display = ('module_question', 'response', 'score')

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('shortname', 'description')

@admin.register(LearningOutcomeSkill)
class LearningOutcomeSkillAdmin(admin.ModelAdmin):
    list_display = ('skill', 'learning_outcome')

@admin.register(QuestionSkill)
class QuestionSkillAdmin(admin.ModelAdmin):
    list_display = ('skill', 'question')