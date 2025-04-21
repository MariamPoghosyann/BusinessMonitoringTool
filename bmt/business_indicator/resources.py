from import_export import resources
from .models import Report

class ReportResources(resources.ModelResource):
    class Meta:
        model = Report
        import_id_fields = ['id']
