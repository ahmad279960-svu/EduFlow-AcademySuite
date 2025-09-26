"""
Database models for the 'enrollment' application.

This module defines the models that track a student's state and progress, such as
which courses they are enrolled in, which lessons they have completed, and their
performance on quizzes. This granular structure is essential for detailed analytics.
"""
import uuid
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

# To avoid circular imports, it's best practice to import apps this way
from apps.learning.models import Course, Lesson, Question, Answer


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
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="enrollments",
        limit_choices_to={"role": "student"},
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


class CompletedLesson(models.Model):
    """
    A through model to track which lessons a student has completed for an enrollment.
    """
    enrollment = models.ForeignKey(Enrollment, on_delete=models.CASCADE, related_name="completed_lessons")
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name="completions")
    completed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("enrollment", "lesson")
        verbose_name = _("Completed Lesson")
        verbose_name_plural = _("Completed Lessons")


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