"""
API Serializers for the 'users' application.

This module provides serializers for the CustomUser model, which control how user
data is converted to and from JSON format for the API endpoints.
"""
from rest_framework import serializers
from apps.users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the CustomUser model.

    This serializer handles the representation of user data. It defines which
    fields are included in the API output. The password field is write-only
    to prevent it from ever being exposed in API responses.
    """
    class Meta:
        """
        Meta options for the serializer.
        """
        model = CustomUser
        fields = [
            "id",
            "username",
            "email",
            "full_name",
            "role",
            "password",
            "avatar_url",
        ]
        extra_kwargs = {
            "password": {"write_only": True, "style": {"input_type": "password"}}
        }

    def create(self, validated_data):
        """
        Creates and returns a new `CustomUser` instance.

        This method overrides the default `create` to ensure that the user's
        password is correctly hashed using Django's `create_user` method.

        :param validated_data: The data that has passed validation.
        :type validated_data: dict
        :returns: The newly created user instance.
        :rtype: apps.users.models.CustomUser
        """
        user = CustomUser.objects.create_user(
            username=validated_data["username"],
            email=validated_data["email"],
            password=validated_data["password"],
            full_name=validated_data.get("full_name"),
            role=validated_data.get("role"),
        )
        return user