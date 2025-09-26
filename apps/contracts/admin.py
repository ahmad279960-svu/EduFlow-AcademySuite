"""
Django admin configuration for the 'contracts' application.

This module registers the Contract model with the admin site and customizes its
interface for usability. For ManyToManyFields, we use inlines with autocomplete
features to efficiently manage relationships.
"""
from django.contrib import admin
from .models import Contract, ContractLearningPath, ContractEnrolledStudent


class ContractLearningPathInline(admin.TabularInline):
    """
    Inline admin for managing the relationship between Contracts and Learning Paths.
    This allows adding/removing learning paths directly on the Contract admin page.
    """
    model = ContractLearningPath
    extra = 1
    autocomplete_fields = ('learning_path',)
    verbose_name = "Associated Learning Path"
    verbose_name_plural = "Associated Learning Paths"


class ContractEnrolledStudentInline(admin.TabularInline):
    """
    Inline admin for managing which students are enrolled under a Contract.
    This allows adding/removing students directly on the Contract admin page.
    """
    model = ContractEnrolledStudent
    extra = 1
    # Use autocomplete_fields for a much better user experience than raw_id_fields.
    autocomplete_fields = ('student',)
    verbose_name = "Enrolled Student under Contract"
    verbose_name_plural = "Enrolled Students under Contract"


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Contract model.

    This configuration uses `inlines` to manage the explicit through models.
    It leverages `autocomplete_fields` within the inlines for an efficient
    and user-friendly way to select related students and learning paths.
    """
    list_display = (
        "title",
        "client",
        "start_date",
        "end_date",
        "is_active",
    )
    list_filter = ("is_active", "client")
    search_fields = ("title", "client__username", "client__full_name")
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {
            "fields": ("title", "client", "is_active")
        }),
        ("Contract Duration", {
            "fields": ("start_date", "end_date")
        }),
        ("Timestamps", {
            "fields": ("created_at", "updated_at"),
            "classes": ("collapse",)
        }),
    )

    inlines = [ContractLearningPathInline, ContractEnrolledStudentInline]