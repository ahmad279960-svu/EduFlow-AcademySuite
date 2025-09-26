"""
API URL configuration for the 'enrollment' application.

This module sets up the URL routing for the enrollment-related API endpoints.
It uses DRF's DefaultRouter to automatically generate the standard URLs for the viewsets.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import EnrollmentViewSet

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r"enrollments", EnrollmentViewSet, basename="enrollment")

# The API URLs are determined automatically by the router.
urlpatterns = [
    path("", include(router.urls)),
]