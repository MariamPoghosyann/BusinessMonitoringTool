from collections import defaultdict

from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from unfold.admin import ModelAdmin
from unfold.contrib.import_export.forms import ExportForm, ImportForm

from business_indicator.models import Report, Deviation
from business_indicator.resources import ReportsResources
from business_indicator.utils import get_deviations


@admin.register(Report)
class ReportAdmin(ModelAdmin, ImportExportModelAdmin):
    resource_class = ReportsResources
    import_form_class = ImportForm
    export_form_class = ExportForm

    list_display = ('business', 'plan_fact', 'date', 'parent_id', 'name')


@admin.register(Deviation)
class DeviationHistoryAdmin(ModelAdmin):
    change_list_template = "deviations_changelist.html"

    def changelist_view(self, request, extra_context=None):

        deviations = get_deviations(request)

        extra_context = {"deviations": deviations}
        grouped_by_business_dict = defaultdict(list)
        for business_deviation in deviations:
            for deviation in business_deviation['data']:
                deviation['is_grow'] = (
                        (deviation['value'] >= 0) == (deviation['pct_deviation_sign'] == 0)
                )
                deviation['color'] = deviation['value'] >= 0

                grouped_by_business_dict[business_deviation['name']].append(deviation)

        return super().changelist_view(request, extra_context=extra_context)

    def get_queryset(self, request):
        return super().get_queryset(request).none()
