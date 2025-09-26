"""
API Views for the 'learning' application.

This module contains the viewsets for the learning API. It provides not only
standard CRUD operations but also custom actions (`@action`) to handle specific
interactive functionalities driven by HTMX, such as reordering lessons in a course.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from apps.learning.models import Course, LearningPath, Lesson, LearningPathCourse
from .serializers import CourseSerializer, LearningPathSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Course instances.

    Includes a custom action to update the order of lessons within a course.
    """
    queryset = Course.objects.prefetch_related('lessons').all()
    serializer_class = CourseSerializer
    # Use more specific permissions in a real app, e.g., IsInstructor.
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'], url_path='update-lesson-order')
    def update_lesson_order(self, request, pk=None):
        """
        Custom action to update the order of lessons in a course.

        Expects a POST request with a payload containing an ordered list of
        lesson IDs, e.g., {'lesson_ids': ['uuid1', 'uuid2', ...]}.
        """
        course = self.get_object()
        lesson_ids = request.data.get('lesson_ids', [])

        if not lesson_ids:
            return Response(
                {'error': 'lesson_ids list is required.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update the order for each lesson
        for index, lesson_id in enumerate(lesson_ids):
            try:
                lesson = Lesson.objects.get(id=lesson_id, course=course)
                lesson.order = index
                lesson.save()
            except Lesson.DoesNotExist:
                # Handle cases where a lesson_id is invalid or doesn't belong to the course
                pass

        return Response({'status': 'success'}, status=status.HTTP_200_OK)


class LearningPathViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing LearningPath instances.

    Includes a custom action to update the structure (course order) of a path.
    """
    queryset = LearningPath.objects.prefetch_related('courses').all()
    serializer_class = LearningPathSerializer
    permission_classes = [IsAdminUser] # Only admins/supervisors should manage paths

    @action(detail=True, methods=['post'], url_path='update-structure')
    def update_structure(self, request, pk=None):
        """
        Custom action to update the courses and their order in a Learning Path.

        Expects a POST request with {'course_ids': ['uuid1', 'uuid2', ...]}.
        It will clear the existing path structure and rebuild it based on the new order.
        """
        learning_path = self.get_object()
        course_ids = request.data.get('course_ids', [])

        # Clear existing course associations for this path
        learning_path.courses.clear()

        # Create new associations with the correct order
        for index, course_id in enumerate(course_ids):
            try:
                course = Course.objects.get(id=course_id)
                LearningPathCourse.objects.create(
                    learning_path=learning_path,
                    course=course,
                    order=index
                )
            except Course.DoesNotExist:
                pass # Ignore invalid course IDs

        return Response({'status': 'structure updated'}, status=status.HTTP_200_OK)