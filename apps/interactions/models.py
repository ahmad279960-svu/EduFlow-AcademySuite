"""
Database models for the 'interactions' application.

This module defines the data structures for user interactions, primarily the
discussion forum, which consists of threads (original questions) and posts (replies).
"""
import uuid
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.learning.models import Lesson


class DiscussionThread(models.Model):
    """
    Represents a single discussion thread, typically an initial question by a student.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="discussion_threads")
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="discussion_threads_started",
    )
    title = models.CharField(_("title"), max_length=255)
    question = models.TextField(_("question"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Discussion Thread")
        verbose_name_plural = _("Discussion Threads")

    def __str__(self):
        return self.title


class DiscussionPost(models.Model):
    """
    Represents a single post or reply within a discussion thread.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    thread = models.ForeignKey(DiscussionThread, on_delete=models.CASCADE, related_name="posts")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="discussion_posts",
    )
    reply_text = models.TextField(_("reply text"))
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["created_at"]
        verbose_name = _("Discussion Post")
        verbose_name_plural = _("Discussion Posts")

    def __str__(self):
        return f"Reply by {self.user.username} on {self.thread.title}"