"""
URL configuration for the 'learning' application.

This module defines the URL patterns for accessing and managing learning content,
including courses, workshops, lessons, learning paths, and quizzes.
"""
from django.urls import path
from . import views

app_name = "learning"

urlpatterns = [
    # --- Content Creation URLs ---
    path("course/create/", views.CourseCreateView.as_view(), name="course-create"),
    path("workshop/create/", views.WorkshopCreateView.as_view(), name="workshop-create"),
    path("path/create/", views.LearningPathCreateView.as_view(), name="path-create"),
    path("course/<uuid:course_pk>/lesson/add/", views.LessonCreateView.as_view(), name="lesson-create-for-course"),
    path("workshop/<uuid:workshop_pk>/lesson/add/", views.LessonCreateView.as_view(), name="lesson-create-for-workshop"),

    # --- Content Management URLs ---
    path("course/<uuid:pk>/manage/", views.CourseManageView.as_view(), name="course-manage"),
    path("workshop/<uuid:pk>/manage/", views.WorkshopManageView.as_view(), name="workshop-manage"),
    path("path/<uuid:pk>/build/", views.PathBuilderView.as_view(), name="path-builder"),
    
    # --- Student Monitoring & Attendance URLs ---
    path("course/<uuid:pk>/progress/", views.CourseStudentProgressView.as_view(), name="course-student-progress"),
    path("enrollment/<uuid:pk>/progress/", views.StudentDetailProgressView.as_view(), name="student-detail-progress"),
    path("lesson/<uuid:pk>/attendance/", views.WorkshopAttendanceView.as_view(), name="workshop-attendance"),

    # --- Content Consumption URLs ---
    path("lesson/<uuid:pk>/", views.LessonDetailView.as_view(), name="lesson-detail"),

    # --- Quiz URLs ---
    path("quiz/<uuid:pk>/take/", views.QuizTakeView.as_view(), name="quiz-take"),
    path("quiz/result/<uuid:attempt_id>/", views.QuizResultView.as_view(), name="quiz-result"),
]