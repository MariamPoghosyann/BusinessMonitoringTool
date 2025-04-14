# from django.contrib import admin, messages
# from django import forms
# from django.urls import path
# from django.shortcuts import render, redirect
# from datetime import datetime
# import csv
#
# from .models import Reports
# from unfold.admin import ModelAdmin  # Make sure Unfold ModelAdmin is used
#
# class CSVUploadForm(forms.Form):
#     csv_file = forms.FileField(label="Upload CSV File")
#
# @admin.register(Reports)
# class ReportsAdmin(ModelAdmin):
#     list_display = ('record_id', 'business', 'date', 'uploaded_by')
#
#     # ✅ This shows the "Import CSV" button at the top of the changelist
#     def get_action_buttons(self, request, context):
#         return [
#             {
#                 "label": "📥 Import CSV",
#                 "url": "import-csv",  # URL pattern we'll define below
#                 "class": "bg-blue-500 text-white",  # optional Tailwind styling
#             }
#         ]
#
#     # ✅ Add the custom URL for file upload
#     def get_urls(self):
#         urls = super().get_urls()
#         custom_urls = [
#             path("import-csv/", self.admin_site.admin_view(self.import_csv), name="reports-import-csv"),
#         ]
#         return custom_urls + urls
#
#     # ✅ View logic to handle CSV upload and import
#     def import_csv(self, request):
#         if request.method == "POST":
#             form = CSVUploadForm(request.POST, request.FILES)
#             if form.is_valid():
#                 file = form.cleaned_data["csv_file"]
#                 decoded = file.read().decode("utf-8").splitlines()
#                 reader = csv.DictReader(decoded)
#
#                 count = 0
#                 for row in reader:
#                     Reports.objects.create(
#                         record_id=row["record_id"],
#                         business=row["business"],
#                         plan_fact=row["plan_fact"],
#                         date=datetime.strptime(row["date"], "%Y-%m-%d").date(),
#                         parent_id=row.get("parent_id") or None,
#                         name=row["name"],
#                         show=row["show"].lower() in ['true', '1'],
#                         type=row["type"],
#                         operation=row["operation"],
#                         reverse_sign=row["reverse_sign"].lower() in ['true', '1'],
#                         value=float(row["value"]),
#                         color_code=row.get("color_code") or None,
#                         uploaded_by=row["uploaded_by"]
#                     )
#                     count += 1
#
#                 self.message_user(request, f"✅ Successfully imported {count} rows.", messages.SUCCESS)
#                 return redirect("..")
#         else:
#             form = CSVUploadForm()
#
#         context = self.admin_site.each_context(request)
#         context["form"] = form
#         context["title"] = "📥 Import CSV"
#         return render(request, "bmt/unfold_crreated/admin/report/import_csv.html", context)  # ✅ Unfold native form view
from import_export.admin import ImportExportModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm

from business_indicator.models import Reports
from django.contrib import admin
from unfold.admin import ModelAdmin
from .resources import ReportsResources

@admin.register(Reports)
class ReportsAdmin(ModelAdmin, ImportExportModelAdmin):
    resource_class = ReportsResources
    import_form_class = ImportForm
    export_form_class = ExportForm

