"""
Custom API permissions for the 'users' application.

This module defines custom permission classes for use with Django REST Framework.
These classes are used to protect API endpoints and ensure that only users with
the appropriate roles can perform certain actions.
"""
from rest_framework.permissions import BasePermission
from apps.users.models import CustomUser


class IsAdminRole(BasePermission):
    """
    Allows access only to users with the 'admin' role.
    """
    def has_permission(self, request, view):
        """
        Check if the user is authenticated and has the 'admin' role.

        :param request: The request object.
        :type request: rest_framework.request.Request
        :param view: The view being accessed.
        :type view: rest_framework.views.APIView
        :returns: True if access is granted, False otherwise.
        :rtype: bool
        """
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == CustomUser.Roles.ADMIN
        )


class IsInstructorRole(BasePermission):
    """
    Allows access only to users with the 'instructor' role.
    """
    def has_permission(self, request, view):
        """
        Check if the user is authenticated and has the 'instructor' role.

        :param request: The request object.
        :type request: rest_framework.request.Request
        :param view: The view being accessed.
        :type view: rest_framework.views.APIView
        :returns: True if access is granted, False otherwise.
        :rtype: bool
        """
        return bool(
            request.user
            and request.user.is_authenticated
            and request.user.role == CustomUser.Roles.INSTRUCTOR
        )