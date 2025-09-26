"""
Root URL configuration for the EduFlow-AcademySuite project.

This module is the primary URL router. It includes the URL patterns for the
built-in Django admin, the various frontend applications, and the versioned
REST API.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# API URL Patterns
api_patterns = [
    path("", include("apps.users.api.urls")),
    path("learning/", include("apps.learning.api.urls")),
    path("enrollment/", include("apps.enrollment.api.urls")),
    path("interactions/", include("apps.interactions.api.urls")),
    path("reports/", include("apps.reports.api.urls")), # New entry for reports API
]

# Main URL Patterns
urlpatterns = [
    # Django Admin
    path("admin/", admin.site.urls),

    # Versioned API
    path("api/v1/", include((api_patterns, "api"), namespace="api")),
    
    # Frontend Application URLs
    path("", include("apps.core.urls", namespace="core")),
    path("users/", include("apps.users.urls", namespace="users")),
    path("learning/", include("apps.learning.urls", namespace="learning")),
    path("enrollment/", include("apps.enrollment.urls", namespace="enrollment")),
    path("interactions/", include("apps.interactions.urls", namespace="interactions")),
    path("contracts/", include("apps.contracts.urls", namespace="contracts")),
    path("reports/", include("apps.reports.urls", namespace="reports")),
]

# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)