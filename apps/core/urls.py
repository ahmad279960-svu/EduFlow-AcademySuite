"""
URL configuration for the 'core' application.

This module defines the essential URL patterns for the application's core
functionality, including authentication (login/logout) and the central dashboard.
"""
from django.urls import path
from django.views.generic import TemplateView
from .views.authentication import CustomLoginView, CustomLogoutView
from .views.dashboards import DashboardView

app_name = "core"

urlpatterns = [
    # The main dashboard view, which routes users based on their role.
    path("dashboard/", DashboardView.as_view(), name="dashboard"),

    # Authentication views
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),

    # The root path serves the main landing page for unauthenticated users.
    # This assumes `landing.html` is in the root `templates` directory.
    path("", TemplateView.as_view(template_name="landing.html"), name="landing"),
]