"""
Unit tests for the 'contracts' application.

This module contains test cases for the Contract model to ensure its relationships
and constraints are working as expected.
"""
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from apps.users.models import CustomUser
from apps.learning.models import LearningPath
from .models import Contract


class ContractModelTest(TestCase):
    """
    Test suite for the Contract model.
    """

    def setUp(self):
        """
        Set up the test environment with necessary user and learning path objects.
        """
        self.client_user = CustomUser.objects.create_user(
            username="b2b_client",
            email="client@company.com",
            password="password",
            role=CustomUser.Roles.THIRD_PARTY,
        )
        self.student_user = CustomUser.objects.create_user(
            username="employee",
            email="employee@company.com",
            password="password",
            role=CustomUser.Roles.STUDENT,
        )
        self.supervisor_user = CustomUser.objects.create_user(
            username="supervisor",
            email="supervisor@edu.com",
            password="password",
            role=CustomUser.Roles.SUPERVISOR,
        )
        self.learning_path = LearningPath.objects.create(
            title="Digital Marketing Diploma",
            description="A full path.",
            supervisor=self.supervisor_user,
        )

    def test_contract_creation(self):
        """
        Test that a Contract instance can be created and relationships established.
        """
        start = timezone.now()
        end = start + timedelta(days=365)
        
        contract = Contract.objects.create(
            title="Company Training 2025",
            client=self.client_user,
            start_date=start,
            end_date=end,
        )

        contract.learning_paths.add(self.learning_path)
        contract.enrolled_students.add(self.student_user)

        self.assertEqual(str(contract), "Company Training 2025")
        self.assertEqual(contract.client.username, "b2b_client")
        self.assertEqual(contract.learning_paths.count(), 1)
        self.assertEqual(contract.enrolled_students.count(), 1)
        self.assertIn(self.learning_path, contract.learning_paths.all())
        self.assertIn(self.student_user, contract.enrolled_students.all())

    def test_client_deletion_protection(self):
        """
        Test that deleting a client user with an active contract is prevented.
        """
        from django.db.models import ProtectedError

        Contract.objects.create(
            title="Protected Contract",
            client=self.client_user,
            start_date=timezone.now(),
            end_date=timezone.now() + timedelta(days=90),
        )

        with self.assertRaises(ProtectedError):
            self.client_user.delete()