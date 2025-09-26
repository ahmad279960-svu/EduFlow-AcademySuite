"""
API URL configuration for the 'reports' application.
"""
from django.urls import path
from .views import AdminDashboardAnalyticsAPI

urlpatterns = [
    path(
        "admin-dashboard-analytics/",
        AdminDashboardAnalyticsAPI.as_view(),
        name="admin-dashboard-analytics"
    ),
]