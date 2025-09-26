"""
API Views for the 'learning' application.

This module contains the viewsets for the learning API. It provides not only
standard CRUD operations but also custom actions (`@action`) to handle specific
interactive functionalities driven by HTMX, such as reordering lessons.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from apps.learning.models import Course, Workshop, LearningPath, Lesson, LearningPathCourse
from .serializers import CourseSerializer, WorkshopSerializer, LearningPathSerializer


class CourseViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Course instances.
    """
    queryset = Course.objects.prefetch_related('lessons').all()
    serializer_class = CourseSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'], url_path='update-lesson-order')
    def update_lesson_order(self, request, pk=None):
        """
        Custom action to update the order of lessons in a course.
        Expects a POST request with a payload of ordered lesson IDs.
        e.g., {'lesson_ids': ['uuid1', 'uuid2', ...]}
        """
        course = self.get_object()
        lesson_ids = request.data.get('lesson_ids', [])

        for index, lesson_id in enumerate(lesson_ids):
            try:
                lesson = Lesson.objects.get(id=lesson_id, course=course)
                lesson.order = index
                lesson.save()
            except Lesson.DoesNotExist:
                # Silently ignore if a lesson_id is invalid or doesn't belong to the course
                pass

        return Response({'status': 'success', 'message': 'Lesson order updated successfully.'}, status=status.HTTP_200_OK)


class WorkshopViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing Workshop instances.
    """
    queryset = Workshop.objects.prefetch_related('lessons').all()
    serializer_class = WorkshopSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'], url_path='update-lesson-order')
    def update_lesson_order(self, request, pk=None):
        """
        Custom action to update the order of lessons in a workshop.
        """
        workshop = self.get_object()
        lesson_ids = request.data.get('lesson_ids', [])

        for index, lesson_id in enumerate(lesson_ids):
            try:
                lesson = Lesson.objects.get(id=lesson_id, workshop=workshop)
                lesson.order = index
                lesson.save()
            except Lesson.DoesNotExist:
                pass

        return Response({'status': 'success', 'message': 'Lesson order updated successfully.'}, status=status.HTTP_200_OK)


class LearningPathViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing LearningPath instances.
    """
    queryset = LearningPath.objects.prefetch_related('courses').all()
    serializer_class = LearningPathSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'], url_path='update-structure')
    def update_structure(self, request, pk=None):
        """
        Custom action to update the courses and their order in a Learning Path.
        """
        learning_path = self.get_object()
        course_ids = request.data.get('course_ids', [])

        learning_path.courses.clear()

        for index, course_id in enumerate(course_ids):
            try:
                course = Course.objects.get(id=course_id)
                LearningPathCourse.objects.create(
                    learning_path=learning_path,
                    course=course,
                    order=index
                )
            except Course.DoesNotExist:
                pass

        return Response({'status': 'structure updated'}, status=status.HTTP_200_OK)