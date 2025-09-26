"""
URL configuration for the 'reports' application.

Defines the URL pattern for the main reports dashboard.
"""
from django.urls import path
from . import views

app_name = "reports"

urlpatterns = [
    path("dashboard/", views.ReportDashboardView.as_view(), name="dashboard"),
]