"""
API Serializers for the 'learning' application.

This module provides serializers for the learning models, controlling their
JSON representation for the API endpoints.
"""
from rest_framework import serializers
from apps.learning.models import Course, Workshop, LearningPath, Lesson


class LessonSerializer(serializers.ModelSerializer):
    """
    Serializer for the Lesson model.
    """
    class Meta:
        model = Lesson
        fields = ["id", "title", "order", "content_type"]


class CourseSerializer(serializers.ModelSerializer):
    """
    Serializer for the Course model.
    """
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Course
        fields = [
            "id",
            "title",
            "slug",
            "description",
            "instructor",
            "category",
            "status",
            "lessons",
        ]


class WorkshopSerializer(serializers.ModelSerializer):
    """
    Serializer for the Workshop model.
    """
    lessons = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Workshop
        fields = [
            "id",
            "title",
            "description",
            "instructor",
            "workshop_type",
            "category",
            "duration_days",
            "total_hours",
            "lessons",
        ]


class LearningPathSerializer(serializers.ModelSerializer):
    """
    Serializer for the LearningPath model.
    """
    courses = CourseSerializer(many=True, read_only=True)

    class Meta:
        model = LearningPath
        fields = ["id", "title", "description", "supervisor", "courses"]