"""
API Serializers for the 'enrollment' application.

This module provides serializers for the enrollment models, controlling their
JSON representation for the API endpoints used by the HTMX frontend.
"""
from rest_framework import serializers
from apps.enrollment.models import Enrollment, QuizAttempt


class EnrollmentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Enrollment model.
    """
    class Meta:
        model = Enrollment
        fields = ["id", "student", "course", "status", "progress"]


class QuizSubmissionSerializer(serializers.Serializer):
    """
    Serializer for validating the payload when a user submits a quiz.
    It expects a dictionary where keys are question IDs and values are the
    selected answer IDs.
    e.g., {"question_id_1": "answer_id_3", "question_id_2": "answer_id_5"}
    """
    answers = serializers.DictField(
        child=serializers.UUIDField(),
        allow_empty=False
    )