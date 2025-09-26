"""
API Views for the 'users' application.

This module contains the viewsets for the user API. It provides the standard
CRUD (Create, Retrieve, Update, Delete) operations for the CustomUser model
through a RESTful interface, protected by appropriate permissions.
"""
from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.views import TokenObtainPairView
from apps.users.models import CustomUser
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.

    This provides a full set of CRUD endpoints for the CustomUser model.
    Access is restricted to users with the 'admin' role via the `IsAdminUser`
    permission class.
    """
    queryset = CustomUser.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom JWT token view.

    This view can be customized in the future to include additional claims
    in the JWT payload, such as the user's role or other profile information.
    Currently, it uses the default behavior.
    """
    # No customization needed yet, but the class is here for future extension.
    pass