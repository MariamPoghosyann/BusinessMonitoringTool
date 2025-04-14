from django.urls import include

from bmt.urls import urlpatterns
from business_indicator.models import Reports

urlpatterns= [
    path('reports/', Report.View(), name='reports'),
    path('api-auth/', include('rest_framework.urls'))
]