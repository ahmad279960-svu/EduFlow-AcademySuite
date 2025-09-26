"""
URL configuration for the 'users' application.

This module defines the URL patterns for the user management frontend. The patterns
map URLs to the corresponding views that handle creating, reading, updating,
and deleting users, designed for an HTMX-powered interface.
"""
from django.urls import path
from . import views

app_name = "users"

urlpatterns = [
    # The main page that hosts the user management interface
    path("manage/", views.UserManagementView.as_view(), name="user-management"),

    # HTMX-powered partial views
    path("list/", views.UserListView.as_view(), name="user-list"),
    path("create/", views.UserCreateView.as_view(), name="user-create"),
    path("<int:pk>/update/", views.UserUpdateView.as_view(), name="user-update"),
    path("<int:pk>/delete/", views.UserDeleteView.as_view(), name="user-delete"),
]