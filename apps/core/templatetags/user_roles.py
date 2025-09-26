"""
Custom template tags and filters for the 'core' application.

This module provides utility functions that can be used directly within Django
templates to simplify logic, such as checking a user's role.
"""
from django import template
from apps.users.models import CustomUser

register = template.Library()


@register.filter(name="has_role")
def has_role(user, role_name):
    """
    A template filter to check if a user has a specific role.

    This allows for conditional rendering in templates based on the user's role,
    for example: {% if request.user|has_role:"admin" %}...{% endif %}

    :param user: The user instance.
    :type user: apps.users.models.CustomUser
    :param role_name: The name of the role to check (e.g., 'admin', 'student').
    :type role_name: str
    :returns: True if the user has the specified role, False otherwise.
    :rtype: bool
    """
    if not isinstance(user, CustomUser):
        return False
    return user.role == role_name