"""
Views for the 'contracts' application.

This module contains views related to B2B contract management, such as the
secure view for B2B clients to export performance reports of their employees.
"""
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404
from django.views import View

from .models import Contract
from apps.reports.services.excel_generator import ExcelReportGenerator


class ExportContractReportView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    A secure view that generates and serves a detailed Excel report for a contract.

    Access is restricted to the B2B client associated with the contract or an
    administrator. This view gathers the necessary data and utilizes the
    ExcelReportGenerator service to produce the final file.
    """

    def test_func(self):
        """
        Checks if the user is authorized to view the report.
        The user must either be an admin or the client linked to the contract.

        :returns: True if the user is authorized, False otherwise.
        :rtype: bool
        """
        self.contract = get_object_or_404(Contract, pk=self.kwargs['contract_pk'])
        user = self.request.user
        return user.role == user.Roles.ADMIN or self.contract.client == user

    def get(self, request, *args, **kwargs):
        """
        Handles the GET request to generate and stream the Excel report.

        It gathers all necessary data, including every enrolled student's progress
        in every relevant course, formats it, and passes it to the report
        generation service.
        """
        contract = self.contract
        students = contract.enrolled_students.prefetch_related(
            "enrollments__course__learning_paths"
        ).order_by('full_name')

        report_data = []
        for student in students:
            # Efficiently filter enrollments relevant to this contract's learning paths.
            enrollments = student.enrollments.filter(
                course__learning_paths__in=contract.learning_paths.all()
            ).distinct()

            if enrollments:
                for enrollment in enrollments:
                    report_data.append({
                        "Student Name": student.full_name or student.username,
                        "Email": student.email,
                        "Course Title": enrollment.course.title,
                        "Progress (%)": enrollment.progress,
                        "Status": enrollment.get_status_display(),
                        "Enrollment Date": enrollment.enrollment_date.strftime("%Y-%m-%d"),
                    })
            else:
                # Include students even if they have no relevant enrollments yet.
                report_data.append({
                    "Student Name": student.full_name or student.username,
                    "Email": student.email,
                    "Course Title": "N/A",
                    "Progress (%)": 0,
                    "Status": "Not Enrolled",
                    "Enrollment Date": "N/A",
                })

        # Structure data for the generator service.
        data_sheets = {
            "Student Progress Report": report_data
        }
        
        report_title = f"Contract_Report_{contract.title.replace(' ', '_')}"
        
        # Utilize the ExcelReportGenerator service from the 'reports' app.
        excel_generator = ExcelReportGenerator(data_sheets=data_sheets, report_filename=report_title)
        return excel_generator.generate()