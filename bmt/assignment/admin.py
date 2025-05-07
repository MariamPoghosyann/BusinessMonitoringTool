from django.contrib import admin
from .models import Assignment
# Register your models here.
admin.site.register(Assignment)

from unfold.contrib.import_export.forms import ExportForm, ImportForm, SelectableFieldsExportForm
