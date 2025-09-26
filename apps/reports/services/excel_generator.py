"""
Excel Generation Service for the 'reports' application.

This module provides a service class that encapsulates the logic for creating
Excel (XLSX) files from structured Python data using the openpyxl library.
"""
from django.http import HttpResponse
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment


class ExcelReportGenerator:
    """
    A service to generate multi-sheet Excel reports from structured data.

    This class is designed to be highly flexible. It takes a dictionary where
    keys are sheet names and values are lists of dictionaries (rows of data).
    It dynamically creates headers and populates the sheets.
    """

    def __init__(self, data_sheets: dict, report_filename: str):
        """
        Initializes the Excel generator.

        :param data_sheets: Data for the report, structured as a dictionary
                            e.g., {"Sheet1": [{"col1": "val", "col2": "val"}], "Sheet2": [...]}.
        :type data_sheets: dict
        :param report_filename: The desired filename for the downloaded report (without extension).
        :type report_filename: str
        """
        self.data_sheets = data_sheets
        self.report_filename = report_filename
        self.workbook = Workbook()

    def generate(self) -> HttpResponse:
        """
        Creates the Excel workbook in memory and returns it as an HttpResponse.

        :returns: An HttpResponse object containing the XLSX file.
        :rtype: django.http.HttpResponse
        """
        # Remove the default sheet created by openpyxl
        self.workbook.remove(self.workbook.active)

        for sheet_name, rows in self.data_sheets.items():
            sheet = self.workbook.create_sheet(title=sheet_name)

            if not rows:
                continue

            # 1. Create headers from the keys of the first dictionary
            headers = list(rows[0].keys())
            sheet.append(headers)

            # Style the header row
            for cell in sheet[1]:
                cell.font = Font(bold=True)
                cell.alignment = Alignment(horizontal="center")

            # 2. Populate data rows
            for row_data in rows:
                sheet.append([row_data.get(header, "") for header in headers])

            # 3. Auto-adjust column widths
            for col in sheet.columns:
                max_length = 0
                column = col[0].column_letter # Get the column name
                for cell in col:
                    try:
                        if len(str(cell.value)) > max_length:
                            max_length = len(cell.value)
                    except:
                        pass
                adjusted_width = (max_length + 2)
                sheet.column_dimensions[column].width = adjusted_width

        # 4. Create the HTTP response
        response = HttpResponse(
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
        response['Content-Disposition'] = f'attachment; filename="{self.report_filename}.xlsx"'

        # Save the workbook to the response's file-like object
        self.workbook.save(response)

        return response