"""
URL configuration for the 'learning' application.

This module defines the URL patterns for accessing learning content, such as
individual lessons, course management pages, and learning path builders.
"""
from django.urls import path
from . import views

app_name = "learning"

urlpatterns = [
    # URL for viewing a specific lesson
    path("lesson/<uuid:pk>/", views.LessonDetailView.as_view(), name="lesson-detail"),

    # URL for the course management interface
    path("course/<uuid:pk>/manage/", views.CourseManageView.as_view(), name="course-manage"),

    # URLs for Learning Paths
    path("path/create/", views.LearningPathCreateView.as_view(), name="path-create"),
    path("path/<uuid:pk>/build/", views.PathBuilderView.as_view(), name="path-builder"),

    # URLs for Quizzes
    path("quiz/<uuid:pk>/take/", views.QuizTakeView.as_view(), name="quiz-take"),
    # The attempt_id here will be a UUID from the enrollment app's QuizAttempt model
    path("quiz/result/<uuid:attempt_id>/", views.QuizResultView.as_view(), name="quiz-result"),
]