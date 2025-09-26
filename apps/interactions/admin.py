"""
Django admin configuration for the 'interactions' application.

This module registers the interaction-related models with the Django admin site
to allow for moderation and management of discussion forums.
"""
from django.contrib import admin
from .models import DiscussionThread, DiscussionPost


class DiscussionPostInline(admin.TabularInline):
    """
    Inline admin for replies within a discussion thread.
    """
    model = DiscussionPost
    extra = 1
    readonly_fields = ('created_at', 'updated_at')


@admin.register(DiscussionThread)
class DiscussionThreadAdmin(admin.ModelAdmin):
    """
    Admin configuration for the DiscussionThread model.
    """
    list_display = ('title', 'lesson', 'student', 'created_at')
    list_filter = ('lesson__course',)
    search_fields = ('title', 'question', 'student__username')
    inlines = [DiscussionPostInline]


@admin.register(DiscussionPost)
class DiscussionPostAdmin(admin.ModelAdmin):
    """
    Admin configuration for the DiscussionPost model.
    """
    list_display = ('id', 'thread', 'user', 'created_at')
    search_fields = ('reply_text', 'user__username', 'thread__title')