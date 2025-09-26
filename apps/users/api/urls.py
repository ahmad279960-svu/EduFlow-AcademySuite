"""
API URL configuration for the 'users' application.

This module sets up the URL routing for the user-related API endpoints. It uses
a DefaultRouter to automatically generate the standard URLs for the UserViewSet
(list, create, retrieve, update, delete). It also includes paths for JWT token
authentication.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView
from .views import UserViewSet, CustomTokenObtainPairView

# Create a router and register our viewsets with it.
router = DefaultRouter()
router.register(r"users", UserViewSet, basename="user")

# The API URLs are determined automatically by the router.
urlpatterns = [
    path("", include(router.urls)),
    path("token/", CustomTokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]