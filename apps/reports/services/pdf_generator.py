"""
PDF Generation Service for the 'reports' application.

This module provides a service class that encapsulates the logic for converting
structured Python data into a formatted PDF file using HTML templates and WeasyPrint.
"""
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML


class PDFReportGenerator:
    """
    A service to generate PDF reports from an HTML template.

    This class takes data, a report title, and a template path, renders the
    HTML, and then converts it into a PDF, returning it as an HttpResponse
    that will trigger a download in the browser.
    """

    def __init__(self, data: list, report_title: str, template_path: str):
        """
        Initializes the PDF generator.

        :param data: A list of dictionaries containing the data for the report.
        :type data: list
        :param report_title: The title of the report.
        :type report_title: str
        :param template_path: The path to the Django template to be rendered.
        :type template_path: str
        """
        self.data = data
        self.report_title = report_title
        self.template_path = template_path

    def generate(self) -> HttpResponse:
        """
        Renders the template and converts it to a PDF.

        :returns: An HttpResponse object containing the PDF file.
        :rtype: django.http.HttpResponse
        """
        context = {
            "report_title": self.report_title,
            "data": self.data,
        }
        # 1. Render the HTML string from the Django template
        html_string = render_to_string(self.template_path, context)

        # 2. Use WeasyPrint to generate the PDF in memory
        html = HTML(string=html_string)
        pdf_file = html.write_pdf()

        # 3. Create an HTTP response with the PDF file
        response = HttpResponse(pdf_file, content_type="application/pdf")
        response['Content-Disposition'] = f'attachment; filename="{self.report_title}.pdf"'

        return response