"""
AppConfig for the 'core' application.

This module defines the configuration for the 'core' Django app, which serves as
the orchestrator and provides the foundational structure for the entire project.
"""

from django.apps import AppConfig


class CoreConfig(AppConfig):
    """
    Configuration class for the 'core' app.

    Sets the default auto field type and the application name. The 'core' app
    is responsible for base templates, static files, and primary navigation views
    like login, logout, and the main dashboard router.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.core"