"""
Views for the 'contracts' application.

This module contains views related to B2B contract management, such as the
secure view for B2B clients to export performance reports of their employees.
"""
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404
from django.views import View

from .models import Contract
# The ExcelReportGenerator will be imported from the 'reports' app once it's built.
# from apps.reports.services.excel_generator import ExcelReportGenerator


class ExportContractReportView(LoginRequiredMixin, UserPassesTestMixin, View):
    """
    A secure view that generates and serves a detailed Excel report for a contract.

    Access is restricted to the B2B client associated with the contract or an admin.
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
        return user.is_staff or self.contract.client == user

    def get(self, request, *args, **kwargs):
        """
        Handles the GET request to generate and stream the Excel report.

        It gathers all necessary data, including every enrolled student's progress
        in every relevant course, and passes it to a dedicated report generation service.
        """
        # The contract object is set in test_func
        contract = self.contract
        students = contract.enrolled_students.prefetch_related(
            "enrollments__course", "enrollments__completed_lessons"
        )

        # 1. Prepare data for the report generator
        report_data = []
        for student in students:
            # This is a simplified data gathering process. A more complex query
            # could be more efficient.
            student_data = {
                "name": student.full_name or student.username,
                "email": student.email,
                "courses": []
            }
            enrollments = student.enrollments.filter(course__learning_paths__in=contract.learning_paths.all()).distinct()

            for enrollment in enrollments:
                student_data["courses"].append({
                    "course_title": enrollment.course.title,
                    "progress": enrollment.progress,
                    "status": enrollment.get_status_display(),
                })
            report_data.append(student_data)
        
        # 2. Call the report generation service (to be implemented in Phase 7)
        # For now, we'll return a placeholder response.
        # excel_generator = ExcelReportGenerator(data=report_data, report_title=f"Report for {contract.title}")
        # excel_file = excel_generator.generate()
        
        # Placeholder response:
        response_content = f"Excel report generation for contract '{contract.title}' is pending the 'reports' app implementation.\n"
        response_content += f"Data gathered for {len(report_data)} student(s)."
        
        response = HttpResponse(
            response_content,
            content_type="text/plain" # "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        # response['Content-Disposition'] = f'attachment; filename="contract_report_{contract.id}.xlsx"'
        
        return response