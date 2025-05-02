# from django.db.models import Sum
from django.shortcuts import render
# from django.views.generic import TemplateView
from rest_framework import viewsets
# from rest_framework.utils.representation import serializer_repr
from .models import Report
from .serializers import ReportsSerializer


class ReportViewSet(viewsets.ModelViewSet):
    def report(self):
        queryset = Report.objects.all()
        serializer_class = ReportsSerializer

    def dashboard_view(request):

        return render(request, 'templates/deviations_changelist.html')

def test_dashboard(request):
    return render(request, 'dashboard.html')


def dashboard_callback(request, context):
    
    context.update({
        "chart_1": {},
        "chart_2": {},
        "custom_variable": "value akdgaksdgahdgajkh",
    })

    return context