"""
AppConfig for the 'reports' application.

This module defines the configuration for the 'reports' Django app. This app
does not have its own user-facing front end but serves as a powerful backend
engine, providing a suite of tools and services for other apps to generate
analytical outputs like PDF and Excel files.
"""

from django.apps import AppConfig


class ReportsConfig(AppConfig):
    """
    Configuration class for the 'reports' app.

    Sets the default auto field type and the application name.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.reports"