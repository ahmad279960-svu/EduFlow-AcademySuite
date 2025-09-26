"""
Database models for the 'contracts' application.

This module defines the data structures for managing B2B contracts, linking
corporate clients to the students (their employees) and the learning paths
they have access to. The relational structure is strict to ensure data integrity.
"""
import uuid
from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from apps.learning.models import LearningPath


class Contract(models.Model):
    """
    Represents a commercial contract with a B2B client.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(_("title"), max_length=255)
    client = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,  # Prevent deleting a client with an active contract
        related_name="contracts_as_client",
        limit_choices_to={"role": "third_party"},
    )
    start_date = models.DateTimeField(_("start date"))
    end_date = models.DateTimeField(_("end date"))
    is_active = models.BooleanField(_("is active"), default=True)

    learning_paths = models.ManyToManyField(
        LearningPath,
        through="ContractLearningPath",
        related_name="contracts",
    )
    enrolled_students = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through="ContractEnrolledStudent",
        related_name="contracts_enrolled_in",
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-start_date"]
        verbose_name = _("Contract")
        verbose_name_plural = _("Contracts")

    def __str__(self):
        return self.title


class ContractLearningPath(models.Model):
    """
    Through model for the Many-to-Many relationship between Contract and LearningPath.
    This explicitly defines the connection.
    """
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    learning_path = models.ForeignKey(LearningPath, on_delete=models.CASCADE)

    class Meta:
        unique_together = ("contract", "learning_path")
        verbose_name = _("Contract Learning Path")
        verbose_name_plural = _("Contract Learning Paths")


class ContractEnrolledStudent(models.Model):
    """
    Through model for the Many-to-Many relationship between Contract and User (Student).
    This records which employees are covered under a specific contract.
    """
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE)
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        limit_choices_to={"role": "student"},
    )

    class Meta:
        unique_together = ("contract", "student")
        verbose_name = _("Contract Enrolled Student")
        verbose_name_plural = _("Contract Enrolled Students")