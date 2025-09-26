"""
Database models for the 'users' application.

This module defines the custom user model for the entire EduFlow-AcademySuite project,
which serves as the single source of truth for user identity and roles.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractUser):
    """
    Custom User model inheriting from Django's AbstractUser.

    This model extends the default user with a `role` field, which is critical for
    the platform's role-based access control (RBAC) system. It also includes
    optional fields for a full name and an avatar URL to enrich the user profile.

    The `username` and `email` fields are enforced as unique.
    """

    class Roles(models.TextChoices):
        """Enumeration for user roles within the system."""
        ADMIN = "admin", _("Admin")
        SUPERVISOR = "supervisor", _("Supervisor")
        INSTRUCTOR = "instructor", _("Instructor")
        STUDENT = "student", _("Student")
        THIRD_PARTY = "third_party", _("B2B Client")

    # The email field is promoted to be unique and required, which is a modern standard.
    email = models.EmailField(_("email address"), unique=True)

    role = models.CharField(
        _("role"),
        max_length=20,
        choices=Roles.choices,
        help_text=_("The role of the user within the system."),
    )
    full_name = models.CharField(
        _("full name"),
        max_length=255,
        blank=True,
        null=True,
        help_text=_("The full name of the user."),
    )
    avatar_url = models.URLField(
        _("avatar URL"),
        max_length=200,
        blank=True,
        null=True,
        help_text=_("URL for the user's avatar image."),
    )

    def __str__(self):
        """
        Returns the string representation of the user.

        :returns: The username of the user.
        :rtype: str
        """
        return self.username

    @property
    def friendly_role(self):
        """
        Returns the display name for the user's role.

        :returns: The human-readable role name.
        :rtype: str
        """
        return self.get_role_display()