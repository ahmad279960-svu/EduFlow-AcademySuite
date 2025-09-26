"""
Django signals for the 'enrollment' application.

This module defines signal receivers that listen for specific events (like model
saves) and trigger side effects, such as dispatching a Celery task to send a
webhook. This helps in decoupling the application's core logic from external
integrations and improves performance.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Enrollment
from apps.core.tasks import send_webhook_task


@receiver(post_save, sender=Enrollment)
def trigger_new_student_onboarding(sender, instance, created, **kwargs):
    """
    Dispatches a task to send a webhook when a new enrollment is created.

    This signal receiver listens for the creation of a new Enrollment instance
    and dispatches the webhook sending logic to a background Celery task. This
    ensures the user's request is not blocked by the external service call.

    :param sender: The model class that sent the signal.
    :param instance: The actual instance being saved.
    :param created: A boolean; True if a new record was created.
    :param kwargs: Keyword arguments.
    """
    if created:
        webhook_url = getattr(settings, "N8N_ENROLLMENT_CREATED_WEBHOOK_URL", None)
        if not webhook_url:
            return

        payload = {
            "student_id": instance.student.id,
            "student_username": instance.student.username,
            "course_id": str(instance.course.id),
            "course_title": instance.course.title,
            "enrollment_date": instance.enrollment_date.isoformat(),
        }

        # Dispatch the task to be executed by a Celery worker in the background.
        send_webhook_task.delay(webhook_url, payload)