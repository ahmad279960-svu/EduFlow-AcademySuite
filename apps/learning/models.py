"""
Database models for the 'learning' application.

This module defines the core data structures for all educational content,
including courses, lessons, learning paths, and their relationships, fully
realizing the relational schema designed for v2.0.
"""
import uuid
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _


class Course(models.Model):
    """
    Represents a single course within the platform.

    A course is a collection of lessons, created and managed by an instructor.
    It has a status to control its visibility and lifecycle.
    """

    class CourseStatus(models.TextChoices):
        DRAFT = "draft", _("Draft")
        PUBLISHED = "published", _("Published")
        ARCHIVED = "archived", _("Archived")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_("title"), max_length=255)
    slug = models.SlugField(_("slug"), max_length=255, unique=True)
    description = models.TextField(_("description"))
    instructor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,  # Prevent deleting an instructor with active courses
        related_name="courses_taught",
        limit_choices_to={"role": "instructor"},
    )
    category = models.CharField(_("category"), max_length=100)
    status = models.CharField(
        _("status"), max_length=20, choices=CourseStatus.choices, default=CourseStatus.DRAFT
    )
    cover_image_url = models.URLField(_("cover image URL"), max_length=200, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = _("Course")
        verbose_name_plural = _("Courses")

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """
    Represents a single lesson within a course.

    A lesson can be of various content types (video, text, quiz). The actual
    content data is stored flexibly in a JSONB field.
    """

    class ContentType(models.TextChoices):
        VIDEO = "video", _("Video")
        TEXT = "text", _("Text")
        QUIZ = "quiz", _("Quiz")
        PDF = "pdf", _("PDF Document")

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name="lessons")
    title = models.CharField(_("title"), max_length=200)
    order = models.PositiveIntegerField(_("order"), default=0)
    content_type = models.CharField(
        _("content type"), max_length=20, choices=ContentType.choices
    )
    content_data = models.JSONField(
        _("content data"),
        help_text=_("Flexible data for content, e.g., {'video_url': '...'}")
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["course", "order"]
        unique_together = ("course", "order")
        verbose_name = _("Lesson")
        verbose_name_plural = _("Lessons")

    def __str__(self):
        return f"{self.course.title} - Lesson {self.order}: {self.title}"


class Question(models.Model):
    """
    Represents a single question within a quiz-type lesson.
    This creates a centralized question bank linked to specific quizzes.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="questions",
        limit_choices_to={"content_type": "quiz"},
    )
    question_text = models.TextField(_("question text"))
    order = models.PositiveIntegerField(_("order"), default=0)

    class Meta:
        ordering = ["lesson", "order"]
        verbose_name = _("Question")
        verbose_name_plural = _("Questions")

    def __str__(self):
        return self.question_text[:50]


class Answer(models.Model):
    """
    Represents a possible answer to a question.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    answer_text = models.CharField(_("answer text"), max_length=500)
    is_correct = models.BooleanField(_("is correct"), default=False)

    class Meta:
        ordering = ["question"]
        verbose_name = _("Answer")
        verbose_name_plural = _("Answers")

    def __str__(self):
        return self.answer_text


class LearningPath(models.Model):
    """
    Represents a learning path or diploma, which is an ordered collection of courses.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_("title"), max_length=255)
    description = models.TextField(_("description"))
    supervisor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="learning_paths_supervised",
        limit_choices_to={"role": "supervisor"},
    )
    courses = models.ManyToManyField(
        Course,
        through="LearningPathCourse",
        related_name="learning_paths",
    )

    class Meta:
        verbose_name = _("Learning Path")
        verbose_name_plural = _("Learning Paths")

    def __str__(self):
        return self.title


class LearningPathCourse(models.Model):
    """
    Through model for the Many-to-Many relationship between LearningPath and Course.

    This model is crucial as it stores the specific order of each course
    within a learning path.
    """
    learning_path = models.ForeignKey(LearningPath, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(_("order"))

    class Meta:
        ordering = ["learning_path", "order"]
        unique_together = ("learning_path", "course")
        verbose_name = _("Learning Path Course")
        verbose_name_plural = _("Learning Path Courses")