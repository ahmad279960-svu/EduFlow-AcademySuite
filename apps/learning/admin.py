"""
Django admin configuration for the 'learning' application.

This module registers the learning-related models with the Django admin site
and provides customizations for a better administrative experience, such as
inlines for managing related objects and search fields for autocomplete functionality.
"""
from django.contrib import admin
from .models import (
    Course,
    Workshop,
    Lesson,
    Question,
    Answer,
    LearningPath,
    LearningPathCourse,
)


class LessonInline(admin.TabularInline):
    """
    Inline admin view for Lessons.
    Allows for adding and editing lessons directly on the parent (Course or Workshop)
    change page. The parent foreign key is dynamically excluded.
    """
    model = Lesson
    extra = 1
    ordering = ("order",)

    def get_formset(self, request, obj=None, **kwargs):
        """
        Dynamically exclude the parent field that is not relevant.
        For example, on a Course admin page, hide the 'workshop' field from the inline.
        """
        if obj:
            if isinstance(obj, Course):
                kwargs['exclude'] = ['workshop']
            elif isinstance(obj, Workshop):
                kwargs['exclude'] = ['course']
        return super().get_formset(request, obj, **kwargs)


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
    autocomplete_fields = ('course',)
    extra = 1
    ordering = ("order",)


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Course model.
    """
    list_display = ("title", "instructor", "category", "status", "created_at")
    list_filter = ("status", "category", "instructor")
    search_fields = ("title", "description", "instructor__username")
    prepopulated_fields = {"slug": ("title",)}
    inlines = [LessonInline]


@admin.register(Workshop)
class WorkshopAdmin(admin.ModelAdmin):
    """
    Admin configuration for the new Workshop model.
    """
    list_display = ("title", "instructor", "workshop_type", "category", "duration_days", "total_hours")
    list_filter = ("workshop_type", "category", "instructor")
    search_fields = ("title", "description", "instructor__username")
    inlines = [LessonInline]


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Lesson model.
    """
    list_display = ('title', 'order', 'content_type')
    list_filter = ('content_type', 'course__title', 'workshop__title')
    # Defining search_fields is crucial for autocomplete to work in other apps.
    search_fields = ('title',)


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Question model.
    """
    list_display = ("question_text", "lesson", "order")
    list_filter = ("lesson__course__title", "lesson__workshop__title")
    search_fields = ("question_text",)
    inlines = [AnswerInline]


@admin.register(LearningPath)
class LearningPathAdmin(admin.ModelAdmin):
    """
    Admin configuration for the LearningPath model.
    """
    list_display = ("title", "supervisor")
    search_fields = ("title", "description", "supervisor__username")
    inlines = [LearningPathCourseInline]


# Registering Answer model with a default admin view
admin.site.register(Answer)