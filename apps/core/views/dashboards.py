"""
Dashboard views for the 'core' application.

This module contains the primary view for routing users to their respective
dashboards based on their assigned role.
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View

from apps.users.models import CustomUser


class DashboardView(LoginRequiredMixin, View):
    """
    A "smart" view that routes users to the correct dashboard.

    This view checks the `role` of the logged-in user and renders the
    appropriate dashboard template. This acts as the central distributor for the
    user experience after login, ensuring each user type sees a relevant and
    tailored interface.
    """

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests by determining the user's role and rendering the dashboard.

        :param request: The HTTP request object.
        :type request: django.http.HttpRequest
        :returns: The rendered dashboard template corresponding to the user's role.
        :rtype: django.http.HttpResponse
        """
        user = request.user
        context = {"user": user}

        # Mapping of user roles to their respective dashboard templates.
        role_to_template = {
            CustomUser.Roles.ADMIN: "dashboards/admin.html",
            CustomUser.Roles.SUPERVISOR: "dashboards/supervisor.html",
            CustomUser.Roles.INSTRUCTOR: "dashboards/instructor.html",
            CustomUser.Roles.STUDENT: "dashboards/student.html",
            CustomUser.Roles.THIRD_PARTY: "dashboards/third_party.html",
        }

        # Default to a generic dashboard or student dashboard if role is not found
        template_name = role_to_template.get(user.role, "dashboards/student.html")

        # Here, you can add role-specific context data fetching.
        # For example, for a student, you might fetch their enrolled courses.
        # if user.role == CustomUser.Roles.STUDENT:
        #     context['enrolled_courses'] = Enrollment.objects.filter(student=user)

        return render(request, template_name, context)