from django.shortcuts import render
from django.views.generic import TemplateView
from rest_framework import viewsets
from rest_framework.utils.representation import serializer_repr
from .models import Report
from .serializers import ReportsSerializer


class ReportViewSet(viewsets.ModelViewSet):
    def report(self):
        queryset = Report.objects.all()
        serializer_class = ReportsSerializer




