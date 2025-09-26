"""
Dashboard views for the 'core' application.

This module contains the primary view for routing users to their respective
dashboards based on their assigned role.
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.views import View
from django.db.models import Count

from apps.users.models import CustomUser
from apps.enrollment.models import Enrollment
from apps.learning.models import Course, LearningPath


class DashboardView(LoginRequiredMixin, View):
    """
    A "smart" view that routes users to the correct dashboard and provides
    role-specific context data.

    This view acts as the central distributor for the user experience after login,
    ensuring each user type sees a relevant, data-driven, and tailored interface.
    """

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests by determining the user's role, fetching relevant
        data from the database, and rendering the appropriate dashboard template.

        :param request: The HTTP request object.
        :type request: django.http.HttpRequest
        :returns: The rendered dashboard template corresponding to the user's role.
        :rtype: django.http.HttpResponse
        """
        user = request.user
        context = {"user": user}

        role_to_template = {
            CustomUser.Roles.ADMIN: "dashboards/admin.html",
            CustomUser.Roles.SUPERVISOR: "dashboards/supervisor.html",
            CustomUser.Roles.INSTRUCTOR: "dashboards/instructor.html",
            CustomUser.Roles.STUDENT: "dashboards/student.html",
            CustomUser.Roles.THIRD_PARTY: "dashboards/third_party.html",
        }

        template_name = role_to_template.get(user.role, "dashboards/student.html")

        # --- Fetch Role-Specific Context Data ---
        
        if user.role == CustomUser.Roles.ADMIN:
            # For the admin, the data is primarily loaded via API for the charts,
            # but we can pass initial KPIs here.
            pass # Data is handled by the API view for the admin dashboard.

        elif user.role == CustomUser.Roles.STUDENT:
            # Fetch the student's enrollments with course and instructor details
            context['enrollments'] = Enrollment.objects.filter(student=user) \
                .select_related('course', 'course__instructor') \
                .order_by('-enrollment_date')

        elif user.role == CustomUser.Roles.INSTRUCTOR:
            # Fetch courses taught by the instructor and aggregate stats
            courses_taught = Course.objects.filter(instructor=user)
            student_count = Enrollment.objects.filter(course__in=courses_taught).values('student').distinct().count()
            context['courses_taught'] = courses_taught
            context['instructor_stats'] = {
                'total_students': student_count,
                'active_courses': courses_taught.filter(status=Course.CourseStatus.PUBLISHED).count(),
                'pending_questions': 0, # Placeholder for interactions query
            }

        elif user.role == CustomUser.Roles.SUPERVISOR:
            # Fetch learning paths supervised by the user
            context['learning_paths'] = LearningPath.objects.filter(supervisor=user)

        elif user.role == CustomUser.Roles.THIRD_PARTY:
            # Fetch contracts associated with the B2B client
            context['contracts'] = user.contracts_as_client.prefetch_related('enrolled_students').all()


        return render(request, template_name, context)