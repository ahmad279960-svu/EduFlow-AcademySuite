# apps/contracts/admin.py

"""
Django admin configuration for the 'contracts' application.

This module registers the Contract model with the admin site and customizes its
interface for usability. For ManyToManyFields with a 'through' model,
we use inlines to manage the relationships directly within the contract page.
"""
from django.contrib import admin
from .models import Contract, ContractLearningPath, ContractEnrolledStudent


class ContractLearningPathInline(admin.TabularInline):
    """
    Inline admin for managing the relationship between Contracts and Learning Paths.
    This allows adding/removing learning paths directly on the Contract admin page.
    """
    model = ContractLearningPath
    extra = 1  # Show one empty slot for adding a new path by default.
    verbose_name = "Associated Learning Path"
    verbose_name_plural = "Associated Learning Paths"


class ContractEnrolledStudentInline(admin.TabularInline):
    """
    Inline admin for managing which students are enrolled under a Contract.
    This allows adding/removing students directly on the Contract admin page.
    """
    model = ContractEnrolledStudent
    extra = 1  # Show one empty slot for adding a new student by default.
    verbose_name = "Enrolled Student under Contract"
    verbose_name_plural = "Enrolled Students under Contract"
    # Use raw_id_fields for better performance with large numbers of users.
    raw_id_fields = ('student',)


@admin.register(Contract)
class ContractAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Contract model.

    This configuration now uses `inlines` to manage the explicit through models,
    which is the correct pattern for ManyToManyFields with a 'through' table.
    The problematic 'filter_horizontal' and direct fieldset entries have been removed.
    """
    list_display = (
        "title",
        "client",
        "start_date",
        "end_date",
        "is_active",
    )
    list_filter = ("is_active", "client")
    search_fields = ("title", "client__username")
    readonly_fields = ('created_at', 'updated_at')
    
    # The main fields of the Contract model itself
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

    # Add the inlines to manage the M2M relationships
    inlines = [ContractLearningPathInline, ContractEnrolledStudentInline]