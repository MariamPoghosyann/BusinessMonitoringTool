from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import viewsets
from rest_framework.utils.representation import serializer_repr
from .models import Reports
from .serializers import ReportsSerializer


class ReportViewSet(viewsets.ModelViewSet):
    def report(self):
        queryset = Reports.objects.all()
        serializer_class = ReportsSerializer




