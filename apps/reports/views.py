"""
Views for the 'reports' application.

This module contains the primary user interface for the reporting engine,
which is a dashboard allowing administrators and supervisors to select,
configure, and generate various system reports.
"""
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render
from django.views import View

from .services.pdf_generator import PDFReportGenerator
from apps.enrollment.models import Enrollment
from apps.users.models import CustomUser


class ReportDashboardView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    A view that displays the report generation dashboard and handles report creation.

    This dashboard provides a user interface with forms and filters that allow
    authorized users to generate specific reports. The actual report generation
    is delegated to dedicated services.
    """

    def test_func(self):
        """
        Ensures only admins and supervisors can access the reports dashboard.
        """
        return self.request.user.role in [CustomUser.Roles.ADMIN, CustomUser.Roles.SUPERVISOR]

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests by rendering the report dashboard template.
        """
        return render(request, "reports/report_dashboard.html")

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests to generate a specific report based on form data.

        This method parses the form data to determine the requested report type
        and filters, fetches the corresponding data, and calls the appropriate
        generation service (e.g., PDFReportGenerator).
        """
        report_type = request.POST.get('report_type')
        
        if report_type == 'student_performance':
            # Fetch data for the student performance report
            enrollments = Enrollment.objects.select_related('student', 'course').filter(
                progress__gt=0
            ).order_by('student__full_name', 'course__title')

            report_data = [
                {
                    "student_name": enrollment.student.full_name or enrollment.student.username,
                    "course_title": enrollment.course.title,
                    "progress": enrollment.progress,
                    "status": enrollment.get_status_display(),
                }
                for enrollment in enrollments
            ]

            # Utilize the PDF generation service
            pdf_service = PDFReportGenerator(
                data=report_data,
                report_title="Student Performance Summary",
                template_path="reports/student_performance_template.html"
            )
            return pdf_service.generate()

        # If other report types are added, they can be handled here.
        return render(request, "reports/report_dashboard.html", {"error": "Invalid report type selected."})