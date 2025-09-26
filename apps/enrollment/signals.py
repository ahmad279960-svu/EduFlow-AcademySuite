"""
Django signals for the 'enrollment' application.

This module defines signal receivers that listen for specific events (like model
saves) and trigger side effects, such as sending a webhook to an external service.
This helps in decoupling the application's core logic from external integrations.
"""
import requests
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Enrollment


@receiver(post_save, sender=Enrollment)
def trigger_new_student_onboarding(sender, instance, created, **kwargs):
    """
    Sends a webhook when a new enrollment is created.

    This signal receiver listens for the creation of a new Enrollment instance
    and sends the relevant data to an external automation service (like n8n)
    to kick off a "New Student Onboarding" workflow.

    :param sender: The model class that sent the signal.
    :param instance: The actual instance being saved.
    :param created: A boolean; True if a new record was created.
    :param kwargs: Keyword arguments.
    """
    if created:
        webhook_url = getattr(settings, "N8N_NEW_ENROLLMENT_WEBHOOK_URL", None)
        if not webhook_url:
            # Silently fail if the webhook URL is not configured
            return

        payload = {
            "student_id": instance.student.id,
            "student_username": instance.student.username,
            "course_id": str(instance.course.id),
            "course_title": instance.course.title,
            "enrollment_date": instance.enrollment_date.isoformat(),
        }

        try:
            # In a production system, this should be an asynchronous task (e.g., using Celery)
            # to avoid blocking the user's request.
            requests.post(webhook_url, json=payload, timeout=5)
        except requests.RequestException:
            # Handle exceptions (e.g., log the error) but don't crash the main request.
            pass