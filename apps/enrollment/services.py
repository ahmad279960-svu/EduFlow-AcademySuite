"""
Business logic services for the 'enrollment' application.

This module isolates complex business logic from the views, such as calculating
a student's progress in a course. This follows the Service Layer pattern.
"""
from .models import Enrollment


def calculate_progress(enrollment_id: str):
    """
    Calculates the progress for a given enrollment and updates the model.

    The progress is calculated as the percentage of completed lessons out of the
    total number of lessons in the course.

    :param enrollment_id: The UUID of the enrollment to update.
    :type enrollment_id: str
    """
    try:
        enrollment = Enrollment.objects.select_related('course').get(id=enrollment_id)
    except Enrollment.DoesNotExist:
        # Handle error appropriately, e.g., log it.
        return

    total_lessons = enrollment.course.lessons.count()
    completed_lessons = enrollment.completed_lessons.count()

    if total_lessons > 0:
        progress = (completed_lessons / total_lessons) * 100
    else:
        progress = 100.0  # Or 0.0, depending on business rule for empty courses

    enrollment.progress = round(progress, 2)

    # Update status to completed if progress is 100%
    if enrollment.progress >= 100.0:
        enrollment.status = Enrollment.EnrollmentStatus.COMPLETED

    enrollment.save(update_fields=['progress', 'status'])