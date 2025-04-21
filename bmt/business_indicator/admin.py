from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm

from business_indicator.models import Report
from django.contrib import admin
from unfold.admin import ModelAdmin
from .resources import ReportResources

@admin.register(Report)
class ReportAdmin(ModelAdmin, ImportExportModelAdmin):
    # resource_class = ReportResources
    import_form_class = ImportForm
    export_form_class = ExportForm

    list_display = ('business', 'plan_fact', 'date', 'parent_id', 'name')
