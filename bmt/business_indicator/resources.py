from import_export import resources
from .models import Reports

class ReportsResources(resources.ModelResource):
    class Meta:
        model = Reports
        import_id_fields = ['id']
