"""
AppConfig for the 'enrollment' application.

This module defines the configuration for the 'enrollment' Django app. This app
is responsible for tracking the state of each student's journey through the
learning content, including course enrollments, lesson completion, and quiz attempts.
"""

from django.apps import AppConfig


class EnrollmentConfig(AppConfig):
    """
    Configuration class for the 'enrollment' app.

    Sets the default auto field type and the application name. It also imports
    the signals module to ensure that the signal handlers are connected when the
    application is ready.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.enrollment"

    def ready(self):
        """
        Imports the signals module when the app is ready.
        """
        import apps.enrollment.signals