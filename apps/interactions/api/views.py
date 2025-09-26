"""
API Views for the 'interactions' application.

This module contains the API endpoints for interactive features, most notably
the endpoint that serves the AI Assistant.
"""
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.shortcuts import get_object_or_404

from .serializers import AIQuestionSerializer
from apps.interactions.services import AIAssistantService
from apps.learning.models import Lesson


class AIAssistantApiView(APIView):
    """
    API view to handle requests to the AI Assistant.

    This view receives a question and lesson context, passes it to the
    AIAssistantService, and returns the AI's response.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests containing the user's question.

        :param request: The HTTP request object.
        :type request: rest_framework.request.Request
        :returns: A JSON response with the AI's answer.
        :rtype: rest_framework.response.Response
        """
        serializer = AIQuestionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = serializer.validated_data
        question = validated_data['question']
        lesson_id = validated_data['lesson_id']

        # Gather context from the database
        lesson = get_object_or_404(Lesson.objects.select_related('course'), pk=lesson_id)
        context = {
            "course_title": lesson.course.title,
            "lesson_title": lesson.title,
        }

        # Call the service to get the response
        ai_service = AIAssistantService()
        answer = ai_service.get_ai_response(question, context)

        return Response({"answer": answer}, status=status.HTTP_200_OK)