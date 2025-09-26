"""
API tests for the 'users' application.

This module contains test cases for the user-related API endpoints, ensuring
that permissions, data serialization, and CRUD operations function as expected.
"""
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from apps.users.models import CustomUser


class UserAPITest(APITestCase):
    """
    Test suite for the User API endpoints.
    """

    def setUp(self):
        """
        Set up the test environment for API tests.
        """
        self.admin_user = CustomUser.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="adminpassword",
            role=CustomUser.Roles.ADMIN,
        )
        self.student_user = CustomUser.objects.create_user(
            username="student",
            email="student@example.com",
            password="studentpassword",
            role=CustomUser.Roles.STUDENT,
        )
        self.list_url = reverse("user-list")
        self.detail_url = reverse("user-detail", kwargs={"pk": self.student_user.pk})

    def test_list_users_unauthenticated(self):
        """
        Ensure unauthenticated users cannot list users.
        """
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_users_non_admin(self):
        """
        Ensure non-admin users cannot list other users.
        """
        self.client.force_authenticate(user=self.student_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_list_users_as_admin(self):
        """
        Ensure admin users can list other users.
        """
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_user_as_admin(self):
        """
        Ensure admin users can retrieve a specific user's details.
        """
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], self.student_user.username)

    def test_create_user_as_admin(self):
        """
        Ensure admin users can create a new user.
        """
        self.client.force_authenticate(user=self.admin_user)
        data = {
            "username": "newinstructor",
            "email": "instructor@example.com",
            "password": "newpassword123",
            "role": "instructor",
        }
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(CustomUser.objects.count(), 3)
        # Check password is hashed and not plain text
        self.assertNotEqual(
            CustomUser.objects.get(username="newinstructor").password,
            "newpassword123",
        )