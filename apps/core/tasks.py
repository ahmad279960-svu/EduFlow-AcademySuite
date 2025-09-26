"""
Asynchronous tasks for the 'core' application.

This module defines Celery tasks that can be executed in the background,
offloading long-running or non-critical operations from the main request-response
cycle. This enhances application performance and reliability.
"""

import requests
from celery import shared_task
from django.conf import settings


@shared_task(bind=True, max_retries=3, default_retry_delay=60)
def send_webhook_task(self, webhook_url: str, payload: dict):
    """
    A Celery task to send a webhook to an external service.

    This task handles the HTTP POST request and includes automatic retries with
    an exponential backoff strategy in case of network failures.

    :param self: The task instance, automatically passed by Celery.
    :param webhook_url: The URL of the external service to notify.
    :type webhook_url: str
    :param payload: The JSON data to send in the request body.
    :type payload: dict
    """
    try:
        response = requests.post(webhook_url, json=payload, timeout=10)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
    except requests.RequestException as exc:
        # If the request fails, Celery will retry the task up to `max_retries` times.
        raise self.retry(exc=exc)