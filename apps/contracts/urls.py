"""
URL configuration for the 'contracts' application.

Defines the URL patterns for contract-related views, such as the endpoint for
exporting B2B client reports.
"""
from django.urls import path
from . import views

app_name = "contracts"

urlpatterns = [
    path(
        "report/<uuid:contract_pk>/export/",
        views.ExportContractReportView.as_view(),
        name="export-report",
    ),
]