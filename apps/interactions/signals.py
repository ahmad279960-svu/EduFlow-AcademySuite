"""
Django signals for the 'interactions' application.

This module defines signal receivers for interaction events, such as a student
posting a new question, to trigger asynchronous external workflows like instructor
notifications via Celery tasks.
"""
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import DiscussionThread
from apps.core.tasks import send_webhook_task


@receiver(post_save, sender=DiscussionThread)
def trigger_new_question_webhook(sender, instance, created, **kwargs):
    """
    Dispatches a task to send a webhook when a new discussion thread is created.

    This is used to notify an external service (like n8n), which can then process
    the event and send a notification to the relevant course instructor, without
    blocking the user's request.

    :param sender: The model class that sent the signal.
    :param instance: The actual instance being saved.
    :param created: A boolean; True if a new record was created.
    :param kwargs: Keyword arguments.
    """
    if created:
        webhook_url = getattr(settings, "N8N_QUESTION_POSTED_WEBHOOK_URL", None)
        if not webhook_url:
            return

        payload = {
            "thread_id": str(instance.id),
            "thread_title": instance.title,
            "question_text": instance.question,
            "student_id": instance.student.id,
            "student_username": instance.student.username,
            "course_id": str(instance.lesson.course.id),
            "course_title": instance.lesson.course.title,
            "lesson_id": str(instance.lesson.id),
            "lesson_title": instance.lesson.title,
            "instructor_email": instance.lesson.course.instructor.email,
        }

        # Dispatch the task to be executed by a Celery worker in the background.
        send_webhook_task.delay(webhook_url, payload)