"""
Database models for the 'enrollment' application.

This module defines the models that track a student's state and progress, such as
which courses they are enrolled in, their progress status for each lesson, and their
performance on quizzes. This granular structure is essential for detailed analytics.
"""
import uuid
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

# To avoid circular imports, models from other apps are imported this way.
from apps.learning.models import Course, Lesson, Question, Answer
from apps.users.models import CustomUser


class Enrollment(models.Model):
    """
    Represents a student's enrollment in a specific course.

    This is the central model for tracking a learner's journey, linking a student
    to a course and storing their overall progress and status.
    """

    class EnrollmentStatus(models.TextChoices):
        IN_PROGRESS = "in_progress", _("In Progress")
        COMPLETED = "completed", _("Completed")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    student = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE,
        related_name="enrollments",
        limit_choices_to={"role": CustomUser.Roles.STUDENT},
    )
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="enrollments")
    enrollment_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(
        _("status"),
        max_length=20,
        choices=EnrollmentStatus.choices,
        default=EnrollmentStatus.IN_PROGRESS,
    )
    progress = models.FloatField(_("progress"), default=0.0, help_text=_("Progress percentage from 0.0 to 100.0"))
    last_accessed_lesson = models.ForeignKey(
        Lesson, on_delete=models.SET_NULL, null=True, blank=True
    )

    class Meta:
        unique_together = ("student", "course")
        ordering = ["-enrollment_date"]
        verbose_name = _("Enrollment")
        verbose_name_plural = _("Enrollments")

    def __str__(self):
        return f"{self.student.username} enrolled in {self.course.title}"


class LessonProgress(models.Model):
    """
    Tracks a student's detailed progress and interaction with a single lesson
    within an enrollment. This replaces the simpler CompletedLesson model.
    """

    class ProgressStatus(models.TextChoices):
        NOT_STARTED = "not_started", _("Not Started")
        IN_PROGRESS = "in_progress", _("In Progress")
        COMPLETED = "completed", _("Completed")
        LATE = "late", _("Late")

    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name="lesson_progress")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="progress_records")
    status = models.CharField(
        _("status"), max_length=20, choices=ProgressStatus.choices, default=ProgressStatus.NOT_STARTED
    )
    attendance_date = models.DateTimeField(_("attendance date"), null=True, blank=True)
    instructor_notes = models.TextField(_("instructor notes"), blank=True)
    student_rating = models.PositiveSmallIntegerField(
        _("student rating"), null=True, blank=True,
        help_text=_("Student's rating of the lesson from 1 to 5")
    )
    started_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("enrollment", "lesson")
        verbose_name = _("Lesson Progress")
        verbose_name_plural = _("Lessons Progress")


class QuizAttempt(models.Model):
    """
    Represents a single attempt by a student on a quiz-type lesson.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name="quiz_attempts")
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="quiz_attempts",
        limit_choices_to={"content_type": "quiz"},
    )
    score = models.FloatField(_("score"), help_text=_("Score percentage from 0.0 to 100.0"))
    submitted_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-submitted_at"]
        verbose_name = _("Quiz Attempt")
        verbose_name_plural = _("Quiz Attempts")

    def __str__(self):
        return f"Attempt by {self.enrollment.student.username} on {self.lesson.title}"


class QuizAnswer(models.Model):
    """
    Records a student's specific answer to a question in a quiz attempt.
    """
    attempt = models.ForeignKey(QuizAttempt, on_delete=models.CASCADE, related_name="user_answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_answer = models.ForeignKey(Answer, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("attempt", "question")
        verbose_name = _("Quiz Answer")
        verbose_name_plural = _("Quiz Answers")