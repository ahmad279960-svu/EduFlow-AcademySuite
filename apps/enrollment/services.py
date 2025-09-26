"""
Business logic services for the 'enrollment' application.

This module isolates complex business logic from the views, such as calculating
a student's progress in a course based on their detailed lesson progress.
This follows the Service Layer pattern for clean architecture.
"""
from .models import Enrollment, LessonProgress


def calculate_progress(enrollment_id: str):
    """
    Calculates the progress for a given enrollment and updates the model.

    The progress is calculated as the percentage of completed lessons out of the
    total number of lessons in the course. This service relies on the detailed
    status from the LessonProgress model.

    :param enrollment_id: The UUID of the enrollment to update.
    :type enrollment_id: str
    """
    try:
        enrollment = Enrollment.objects.select_related('course').get(id=enrollment_id)
    except Enrollment.DoesNotExist:
        # Handle error appropriately, e.g., log it.
        return

    total_lessons = enrollment.course.lessons.count()
    completed_lessons = enrollment.lesson_progress.filter(
        status=LessonProgress.ProgressStatus.COMPLETED
    ).count()

    if total_lessons > 0:
        progress = (completed_lessons / total_lessons) * 100
    else:
        # If a course has no lessons, it is considered 100% complete upon enrollment.
        progress = 100.0

    enrollment.progress = round(progress, 2)

    # Update enrollment status to completed if progress reaches 100%
    if enrollment.progress >= 100.0:
        enrollment.status = Enrollment.EnrollmentStatus.COMPLETED
    else:
        enrollment.status = Enrollment.EnrollmentStatus.IN_PROGRESS

    enrollment.save(update_fields=['progress', 'status'])