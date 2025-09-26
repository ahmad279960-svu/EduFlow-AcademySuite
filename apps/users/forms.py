"""
Django Forms for the 'users' application.

This module provides custom forms for creating and updating CustomUser instances,
ensuring that custom fields like 'role' and 'full_name' are properly handled
and validated. These forms are used in the Django admin and can also be leveraged
in the frontend for user management tasks.
"""
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    A form for creating new users.

    This form extends Django's `UserCreationForm` to include the custom fields
    defined in the `CustomUser` model. It specifies the fields required for user
    creation and links them to the CustomUser model.
    """
    class Meta(UserCreationForm.Meta):
        """
        Meta options for the form.
        """
        model = CustomUser
        fields = ("username", "email", "full_name", "role")


class CustomUserChangeForm(UserChangeForm):
    """
    A form for updating existing users.

    This form extends Django's `UserChangeForm` for use in the admin interface
    to modify user details. It includes the custom fields from the `CustomUser` model.
    """
    class Meta:
        """
        Meta options for the form.
        """
        model = CustomUser
        fields = ("username", "email", "full_name", "role", "is_active", "is_staff")