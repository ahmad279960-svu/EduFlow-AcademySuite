"""
AppConfig for the 'interactions' application.

This module defines the configuration for the 'interactions' Django app, which
manages all forms of communication and social engagement within the platform,
such as discussion forums and the AI assistant.
"""

from django.apps import AppConfig


class InteractionsConfig(AppConfig):
    """
    Configuration class for the 'interactions' app.

    Sets the default auto field type and the application name. It also imports
    the signals module to ensure that signal handlers are connected when the
    application is ready.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.interactions"

    def ready(self):
        """
        Imports the signals module when the app is ready.
        """
        import apps.interactions.signals