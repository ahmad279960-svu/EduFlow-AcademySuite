# apps/core/views/authentication.py

"""
Authentication-related views for the 'core' application.

This module handles the logic for user login and logout, extending Django's
built-in views to use custom templates and redirect logic consistent with the
application's flow.
"""
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy


class CustomLoginView(auth_views.LoginView):
    """
    A custom view for handling user login.

    This view extends Django's default `LoginView` to specify a custom template
    for the login page. Upon successful login, it redirects the user to the
    main dashboard. It also redirects already authenticated users away from the
    login page.
    """
    template_name = "login.html"
    redirect_authenticated_user = True
    next_page = reverse_lazy("core:dashboard")


class CustomLogoutView(auth_views.LogoutView):
    """
    A custom view for handling user logout.

    This view extends Django's default `LogoutView` to specify a redirect
    location after a user logs out, sending them to the main landing page.
    """
    # The fix is here: we specify the namespace 'core' before 'landing'.
    next_page = reverse_lazy("core:landing")