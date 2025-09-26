"""
API Serializers for the 'interactions' application.

This module provides serializers for validating input to the interaction-related
API endpoints, such as the AI Assistant.
"""
from rest_framework import serializers


class AIQuestionSerializer(serializers.Serializer):
    """
    Serializer to validate the question and context for the AI Assistant API.
    """
    question = serializers.CharField(max_length=2000, required=True)
    lesson_id = serializers.UUIDField(required=True)