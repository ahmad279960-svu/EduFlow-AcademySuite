"""
Unit tests for the 'users' application models.

This module contains test cases for the CustomUser model to ensure its
functionality, including role management and string representation.
"""
from django.test import TestCase
from apps.users.models import CustomUser


class CustomUserModelTest(TestCase):
    """
    Test suite for the CustomUser model.
    """

    def setUp(self):
        """
        Set up the test environment.

        Creates a user instance that can be used across multiple test methods.
        """
        self.user = CustomUser.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpassword123",
            role=CustomUser.Roles.STUDENT,
            full_name="Test User",
        )

    def test_user_creation(self):
        """
        Test that a CustomUser instance is created correctly.
        """
        self.assertEqual(self.user.username, "testuser")
        self.assertEqual(self.user.email, "test@example.com")
        self.assertEqual(self.user.role, "student")
        self.assertEqual(self.user.full_name, "Test User")
        self.assertTrue(self.user.is_active)
        self.assertFalse(self.user.is_staff)
        self.assertFalse(self.user.is_superuser)

    def test_string_representation(self):
        """
        Test the __str__ method of the CustomUser model.
        """
        self.assertEqual(str(self.user), "testuser")

    def test_friendly_role_property(self):
        """
        Test the `friendly_role` property.
        """
        self.assertEqual(self.user.friendly_role, "Student")

    def test_email_is_unique(self):
        """
        Test that the email field enforces uniqueness.
        """
        from django.db.utils import IntegrityError

        with self.assertRaises(IntegrityError):
            CustomUser.objects.create_user(
                username="anotheruser",
                email="test@example.com",  # Same email
                password="anotherpassword",
                role=CustomUser.Roles.INSTRUCTOR,
            )