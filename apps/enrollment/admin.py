"""
Django admin configuration for the 'enrollment' application.

This module registers the enrollment-related models with the Django admin site,
allowing administrators to view and manage student progress and quiz data.
"""
from django.contrib import admin
from .models import Enrollment, CompletedLesson, QuizAttempt, QuizAnswer


class CompletedLessonInline(admin.TabularInline):
    """
    Inline admin for CompletedLesson within an Enrollment.
    """
    model = CompletedLesson
    extra = 0
    readonly_fields = ('lesson', 'completed_at')


class QuizAttemptInline(admin.TabularInline):
    """
    Inline admin for QuizAttempt within an Enrollment.
    """
    model = QuizAttempt
    extra = 0
    readonly_fields = ('lesson', 'score', 'submitted_at')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Enrollment model.
    """
    list_display = ("student", "course", "status", "progress", "enrollment_date")
    list_filter = ("status", "course")
    search_fields = ("student__username", "course__title")
    readonly_fields = ("enrollment_date",)
    inlines = [CompletedLessonInline, QuizAttemptInline]


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    """
    Admin configuration for the QuizAttempt model.
    """
    list_display = ('id', 'enrollment', 'lesson', 'score', 'submitted_at')
    list_filter = ('lesson__course',)
    search_fields = ('enrollment__student__username', 'lesson__title')


@admin.register(QuizAnswer)
class QuizAnswerAdmin(admin.ModelAdmin):
    """
    Admin configuration for the QuizAnswer model.
    """
    list_display = ('attempt', 'question', 'selected_answer')
    search_fields = ('attempt__enrollment__student__username',)