"""
AppConfig for the 'users' application.

This module defines the configuration for the 'users' Django app, which is responsible
for identity and access management within the EduFlow-AcademySuite system.
"""

from django.apps import AppConfig


class UsersConfig(AppConfig):
    """
    Configuration class for the 'users' app.

    This class sets the default auto field type and the application name.
    The name 'apps.users' is used to ensure the app can be correctly located
    within the 'apps' directory, following the project's modular structure.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.users"