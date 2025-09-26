"""
Django admin configuration for the 'enrollment' application.

This module registers the enrollment-related models with the Django admin site,
allowing administrators to view and manage student progress, attendance,
and quiz data in a detailed manner.
"""
from django.contrib import admin
from .models import Enrollment, LessonProgress, QuizAttempt, QuizAnswer


class LessonProgressInline(admin.TabularInline):
    """
    Inline admin for LessonProgress within an Enrollment.
    Provides a detailed view of each lesson's status for the student.
    """
    model = LessonProgress
    extra = 0
    fields = ('lesson', 'status', 'attendance_date', 'student_rating', 'instructor_notes')
    readonly_fields = ('lesson',)
    autocomplete_fields = ('lesson',)


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
    list_filter = ("status", "course__title")
    search_fields = ("student__username", "course__title")
    readonly_fields = ("enrollment_date",)
    inlines = [LessonProgressInline, QuizAttemptInline]


@admin.register(QuizAttempt)
class QuizAttemptAdmin(admin.ModelAdmin):
    """
    Admin configuration for the QuizAttempt model.
    """
    list_display = ('id', 'enrollment', 'lesson', 'score', 'submitted_at')
    list_filter = ('lesson__course__title',)
    search_fields = ('enrollment__student__username', 'lesson__title')


@admin.register(QuizAnswer)
class QuizAnswerAdmin(admin.ModelAdmin):
    """
    Admin configuration for the QuizAnswer model.
    """
    list_display = ('attempt', 'question', 'selected_answer')
    search_fields = ('attempt__enrollment__student__username',)