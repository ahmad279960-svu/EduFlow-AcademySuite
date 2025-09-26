"""
Views for the 'users' application.

This module contains the views that handle the frontend logic for user management,
such as displaying, creating, updating, and deleting users. These views are
designed to work with HTMX to provide a dynamic, single-page application-like
experience for administrators.
"""
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views.generic import (
    View,
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
)
from .models import CustomUser
from .forms import CustomUserChangeForm, CustomUserCreationForm


class AdminRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    """
    Mixin to ensure the user has the 'admin' role.

    This is a security measure to restrict access to user management views
    to only administrators.
    """

    def test_func(self):
        """
        Checks if the user has the 'admin' role.

        :returns: True if the user is an admin, False otherwise.
        :rtype: bool
        """
        return self.request.user.role == CustomUser.Roles.ADMIN


class UserManagementView(AdminRequiredMixin, View):
    """
    A container view that renders the main user management page.

    This view serves the main template which acts as a host for the dynamic
    HTMX-powered components like the user list and forms.
    """
    def get(self, request, *args, **kwargs):
        """
        Handles GET requests to render the user management page.

        :param request: The HTTP request object.
        :type request: django.http.HttpRequest
        :returns: The rendered user management template.
        :rtype: django.http.HttpResponse
        """
        return render(request, "users/user_management.html")


class UserListView(AdminRequiredMixin, ListView):
    """
    View to list and search users.

    This view is designed to be called via HTMX. It returns an HTML fragment
    containing the list of users, which is then swapped into the main
    user management page. It supports search functionality based on a query parameter.
    """
    model = CustomUser
    template_name = "partials/_user_list.html"
    context_object_name = "users"

    def get_queryset(self):
        """
        Filters the user list based on a search query.

        The search query is retrieved from the 'q' GET parameter and filters
        users by username, email, or full name.

        :returns: A queryset of filtered users.
        :rtype: django.db.models.QuerySet
        """
        queryset = super().get_queryset().order_by("username")
        query = self.request.GET.get("q")
        if query:
            return queryset.filter(
                models.Q(username__icontains=query) |
                models.Q(email__icontains=query) |
                models.Q(full_name__icontains=query)
            )
        return queryset


class UserCreateView(AdminRequiredMixin, CreateView):
    """
    View for creating a new user.

    This view handles both the display of the user creation form (in a modal)
    and the processing of the form submission. It is called via HTMX. On successful
    creation, it sends a custom HTMX trigger to the client to refresh the user list.
    """
    model = CustomUser
    form_class = CustomUserCreationForm
    template_name = "users/_user_form.html"

    def form_valid(self, form):
        """
        Processes a valid form submission.

        Saves the new user and returns an empty response with an HTMX trigger
        header to signal success to the frontend.

        :param form: The validated form instance.
        :type form: CustomUserCreationForm
        :returns: An empty HTTP response with a trigger header.
        :rtype: django.http.HttpResponse
        """
        form.save()
        response = HttpResponse(status=204)
        response["HX-Trigger"] = "userListChanged"
        return response


class UserUpdateView(AdminRequiredMixin, UpdateView):
    """
    View for updating an existing user.

    Similar to UserCreateView, this view handles displaying the update form and
    processing its submission via HTMX. On success, it triggers a refresh
    of the user list.
    """
    model = CustomUser
    form_class = CustomUserChangeForm
    template_name = "users/_user_form.html"
    context_object_name = "user"

    def form_valid(self, form):
        """
        Processes a valid form submission for updating a user.

        :param form: The validated form instance.
        :type form: CustomUserChangeForm
        :returns: An empty HTTP response with a trigger header.
        :rtype: django.http.HttpResponse
        """
        form.save()
        response = HttpResponse(status=204)
        response["HX-Trigger"] = "userListChanged"
        return response


class UserDeleteView(AdminRequiredMixin, DeleteView):
    """
    View for deleting a user.

    This view handles user deletion. Since it's a `DeleteView`, it expects a POST
    request to perform the deletion. On successful deletion, it returns an empty
    response with a trigger to refresh the user list on the frontend.
    """
    model = CustomUser
    # On success, we don't redirect. HTMX will handle the UI update.
    success_url = reverse_lazy("users:user-list") # Placeholder, not used by HTMX

    def delete(self, request, *args, **kwargs):
        """
        Handles the deletion of a user object.

        :param request: The HTTP request object.
        :type request: django.http.HttpRequest
        :returns: An empty HTTP response with a trigger header.
        :rtype: django.http.HttpResponse
        """
        self.object = self.get_object()
        self.object.delete()
        response = HttpResponse(status=204)
        # We can also choose to trigger a full page reload or a specific target refresh.
        response["HX-Trigger"] = "userListChanged"
        return response

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests by simply returning the confirmation form.
        A more robust implementation could render a confirmation modal.
        For now, this is handled on the client-side.
        """
        user = get_object_or_404(CustomUser, pk=kwargs.get('pk'))
        return render(request, 'partials/_delete_confirm.html', {'object': user})