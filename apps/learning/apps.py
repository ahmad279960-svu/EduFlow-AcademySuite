"""
AppConfig for the 'learning' application.

This module defines the configuration for the 'learning' Django app, which is the
most complex in terms of data structure. It manages all educational entities
such as Courses, Lessons, Learning Paths, and Quizzes.
"""

from django.apps import AppConfig


class LearningConfig(AppConfig):
    """
    Configuration class for the 'learning' app.

    Sets the default auto field type and the application name.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.learning"