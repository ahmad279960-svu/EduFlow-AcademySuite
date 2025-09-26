"""
API URL configuration for the 'learning' application.

This module sets up the URL routing for the learning-related API endpoints using
DRF's DefaultRouter to automatically generate standard URLs for the viewsets.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CourseViewSet, LearningPathViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r"courses", CourseViewSet, basename="course")
router.register(r"learning-paths", LearningPathViewSet, basename="learningpath")

# The API URLs are determined automatically by the router.
urlpatterns = [
    path("", include(router.urls)),
]