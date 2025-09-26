"""
Django admin configuration for the 'users' application.

This module registers the CustomUser model with the Django admin site and
customizes its appearance and functionality for administrative purposes.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser
from .forms import CustomUserChangeForm, CustomUserCreationForm


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    """
    Admin configuration for the CustomUser model.

    This class extends the default `UserAdmin` to integrate the custom fields
    (`role`, `full_name`) into the admin interface. It specifies which fields
    are displayed in the list view, used in creation/change forms, and available
    for filtering.
    """
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser

    list_display = [
        "username",
        "email",
        "full_name",
        "role",
        "is_staff",
        "is_active",
    ]
    list_filter = ["role", "is_staff", "is_superuser", "is_active", "groups"]

    # Fieldsets for the user detail/edit page.
    # The structure is inherited from UserAdmin and extended with the 'Custom Fields' section.
    fieldsets = UserAdmin.fieldsets + (
        ("Custom Fields", {"fields": ("full_name", "role", "avatar_url")}),
    )

    # Fields to be displayed when creating a new user.
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Custom Fields", {"fields": ("full_name", "role", "avatar_url")}),
    )