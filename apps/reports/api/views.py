"""
API Views for the 'reports' application.

This module contains the API endpoints that provide data for the dynamic
charts and analytics displayed on the various user dashboards.
"""
from django.db.models import Count, Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser
from apps.users.models import CustomUser
from apps.learning.models import Course
from apps.enrollment.models import Enrollment

class AdminDashboardAnalyticsAPI(APIView):
    """
    API view to provide analytics data for the Admin Dashboard.

    This endpoint aggregates key platform metrics, such as user role distribution,
    course enrollment statistics, and user registration trends, and is protected
    to be accessible only by administrators.
    """
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and returns a JSON response with dashboard data.

        :param request: The HTTP request object.
        :type request: rest_framework.request.Request
        :returns: A JSON response containing aggregated analytics data.
        :rtype: rest_framework.response.Response
        """
        # User Role Distribution
        role_distribution = (
            CustomUser.objects.values('role')
            .annotate(count=Count('id'))
            .order_by('-count')
        )
        
        # Top 5 Most Enrolled Courses
        top_courses = (
            Course.objects.annotate(enrollment_count=Count('enrollments'))
            .order_by('-enrollment_count')
            .values('title', 'enrollment_count')[:5]
        )

        # Platform-wide Statistics
        platform_stats = {
            "total_users": CustomUser.objects.count(),
            "total_courses": Course.objects.count(),
            "total_enrollments": Enrollment.objects.count(),
            "completed_enrollments": Enrollment.objects.filter(status=Enrollment.EnrollmentStatus.COMPLETED).count(),
        }

        data = {
            "role_distribution": list(role_distribution),
            "top_courses": list(top_courses),
            "platform_stats": platform_stats,
        }

        return Response(data)