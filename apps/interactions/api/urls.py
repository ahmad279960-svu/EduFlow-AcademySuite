"""
API URL configuration for the 'interactions' application.

Defines the URL pattern for the AI Assistant API endpoint.
"""
from django.urls import path
from .views import AIAssistantApiView

urlpatterns = [
    path("ai-assistant/", AIAssistantApiView.as_view(), name="ai-assistant"),
]