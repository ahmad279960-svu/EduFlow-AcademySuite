"""
URL configuration for the 'enrollment' application.

This module is currently minimal as most of the user-facing enrollment logic
is handled via the API and integrated into the 'learning' app's templates.
It can be expanded to include pages like a student's certificate gallery.
"""
from django.urls import path

app_name = "enrollment"

urlpatterns = [
    # Placeholder for future frontend views, e.g., a "My Certificates" page.
]