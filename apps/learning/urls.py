"""
URL configuration for the 'learning' application.

This module defines the URL patterns for accessing and managing learning content,
including courses, workshops, lessons, learning paths, and quizzes.
"""
from django.urls import path
from . import views

app_name = "learning"

urlpatterns = [
    # Content Consumption URLs
    path("lesson/<uuid:pk>/", views.LessonDetailView.as_view(), name="lesson-detail"),

    # Course Management URLs
    path("course/<uuid:pk>/manage/", views.CourseManageView.as_view(), name="course-manage"),
    
    # Workshop Management URLs
    path("workshop/<uuid:pk>/manage/", views.WorkshopManageView.as_view(), name="workshop-manage"),

    # Learning Path Management URLs
    path("path/create/", views.LearningPathCreateView.as_view(), name="path-create"),
    path("path/<uuid:pk>/build/", views.PathBuilderView.as_view(), name="path-builder"),

    # Quiz URLs
    path("quiz/<uuid:pk>/take/", views.QuizTakeView.as_view(), name="quiz-take"),
    path("quiz/result/<uuid:attempt_id>/", views.QuizResultView.as_view(), name="quiz-result"),
]