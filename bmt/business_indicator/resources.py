from django.core.cache import cache
from import_export import resources
from business.models import Business
from .models import Report

class ReportsResources(resources.ModelResource):
    class Meta:
        model = Report
        import_id_fields = ['record_id', 'date', 'plan_fact']

    def before_import(self, dataset, **kwargs):
        dataset.headers[0] = 'record_id'
        return dataset

    def before_import_row(self, row, **kwargs):
        business_name = row.get('business')

        if business_name:
            business, _ = Business.objects.get_or_create(name=business_name)  # Get the Business object by name
            row['business'] = business.id

    def after_import(self, dataset, result, **kwargs):
        cache.clear()

