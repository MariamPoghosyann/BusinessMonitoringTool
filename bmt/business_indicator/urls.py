# from django.urls import include
#
# from bmt.urls import urlpatterns
# from business_indicator.models import Report
#
from os import path

urlpatterns= [
    path('dashboard/', dashboard_view, name='reports'),
    # path('api-auth/', include('rest_framework.urls'))
]
