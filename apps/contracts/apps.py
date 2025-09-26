"""
AppConfig for the 'contracts' application.

This module defines the configuration for the 'contracts' Django app, which
is the bridge between the system and its B2B clients. It provides the necessary
tools to manage commercial agreements and track corporate user progress.
"""

from django.apps import AppConfig


class ContractsConfig(AppConfig):
    """
    Configuration class for the 'contracts' app.

    Sets the default auto field type and the application name.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.contracts"