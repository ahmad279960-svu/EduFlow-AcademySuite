"""
API Views for the 'enrollment' application.

This module contains the core API logic for a student's interaction with a course,
including marking lessons as complete and submitting quizzes. These actions are
exposed as custom actions on a viewset and are designed to be called via HTMX.
"""
from django.shortcuts import get_object_or_404
from django.urls import reverse
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.enrollment.models import Enrollment, CompletedLesson, QuizAttempt, QuizAnswer
from apps.learning.models import Lesson, Answer
from apps.enrollment.services import calculate_progress
from .serializers import EnrollmentSerializer, QuizSubmissionSerializer


class EnrollmentViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A viewset for handling student enrollments and course interactions.

    This viewset is primarily read-only for the enrollment list but provides
    critical custom actions for course progression.
    """
    queryset = Enrollment.objects.all()
    serializer_class = EnrollmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Users can only see their own enrollments.
        """
        return self.queryset.filter(student=self.request.user)

    @action(detail=True, methods=['post'], url_path='mark-lesson-complete')
    def mark_lesson_complete(self, request, pk=None):
        """
        Marks a specific lesson as complete for the given enrollment.

        Expects a POST request with {'lesson_id': 'uuid'}.
        """
        enrollment = self.get_object()
        lesson_id = request.data.get('lesson_id')
        lesson = get_object_or_404(Lesson, id=lesson_id, course=enrollment.course)

        # Create the completion record if it doesn't exist.
        CompletedLesson.objects.get_or_create(enrollment=enrollment, lesson=lesson)

        # Update the last accessed lesson
        enrollment.last_accessed_lesson = lesson
        enrollment.save(update_fields=['last_accessed_lesson'])

        # Recalculate and update the overall course progress.
        calculate_progress(enrollment.id)

        # Refresh the enrollment object to get the latest progress
        enrollment.refresh_from_db()

        return Response(
            {'status': 'success', 'progress': enrollment.progress},
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'], url_path='submit-quiz')
    def submit_quiz(self, request, pk=None):
        """
        Submits answers for a quiz, calculates the score, and stores the attempt.

        Expects a POST request with {'lesson_id': 'uuid', 'answers': {'q_uuid': 'a_uuid', ...}}.
        """
        enrollment = self.get_object()
        lesson_id = request.data.get('lesson_id')
        lesson = get_object_or_404(
            Lesson, id=lesson_id, course=enrollment.course, content_type=Lesson.ContentType.QUIZ
        )

        serializer = QuizSubmissionSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        answers_data = serializer.validated_data['answers']
        total_questions = lesson.questions.count()
        correct_answers = 0

        # Create the attempt object first
        attempt = QuizAttempt.objects.create(enrollment=enrollment, lesson=lesson, score=0)

        # Validate answers and calculate score
        for question_id, answer_id in answers_data.items():
            try:
                correct_answer = Answer.objects.get(question_id=question_id, is_correct=True)
                if str(correct_answer.id) == answer_id:
                    correct_answers += 1
                
                # Record the user's answer
                selected_answer = Answer.objects.get(id=answer_id)
                QuizAnswer.objects.create(
                    attempt=attempt,
                    question_id=question_id,
                    selected_answer=selected_answer
                )
            except Answer.DoesNotExist:
                # Handle cases where an invalid answer or question ID is submitted
                pass

        score = (correct_answers / total_questions) * 100 if total_questions > 0 else 100.0
        attempt.score = round(score, 2)
        attempt.save()
        
        # Mark the quiz lesson as complete after submission
        CompletedLesson.objects.get_or_create(enrollment=enrollment, lesson=lesson)
        calculate_progress(enrollment.id)

        result_url = reverse('learning:quiz-result', kwargs={'attempt_id': attempt.id})
        return Response({'status': 'success', 'score': attempt.score, 'result_url': result_url}, status=status.HTTP_200_OK)