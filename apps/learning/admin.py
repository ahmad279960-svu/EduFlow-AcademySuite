"""
Django admin configuration for the 'learning' application.

This module registers the learning-related models with the Django admin site
and provides customizations for a better administrative experience, such as
inlines for managing related objects.
"""
from django.contrib import admin
from .models import (
    Course,
    Lesson,
    Question,
    Answer,
    LearningPath,
    LearningPathCourse,
)


class LessonInline(admin.TabularInline):
    """
    Inline admin view for Lessons within a Course.
    Allows for adding and editing lessons directly on the course change page.
    """
    model = Lesson
    extra = 1
    ordering = ("order",)


class AnswerInline(admin.TabularInline):
    """
    Inline admin view for Answers within a Question.
    """
    model = Answer
    extra = 3


class LearningPathCourseInline(admin.TabularInline):
    """
    Inline admin view for Courses within a Learning Path.
    """
    model = LearningPathCourse
    extra = 1
    ordering = ("order",)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Course model.
    """
    list_display = ("title", "instructor", "category", "status", "created_at")
    list_filter = ("status", "category", "instructor")
    search_fields = ("title", "description")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [LessonInline]


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Question model.
    """
    list_display = ("question_text", "lesson", "order")
    list_filter = ("lesson__course",)
    search_fields = ("question_text",)
    inlines = [AnswerInline]


@admin.register(LearningPath)
class LearningPathAdmin(admin.ModelAdmin):
    """
    Admin configuration for the LearningPath model.
    """
    list_display = ("title", "supervisor")
    search_fields = ("title", "description")
    inlines = [LearningPathCourseInline]


# Registering other models with default admin views
admin.site.register(Lesson)
admin.site.register(Answer)