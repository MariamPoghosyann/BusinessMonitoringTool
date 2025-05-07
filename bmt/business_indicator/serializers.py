from rest_framework import serializers

from business.models import Business
from .models import Report

class ReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'

class CSVUploaderSerializer(serializers.Serializer):
    file = serializers.FileField()

class BusinessSerializer(serializers.ModelSerializer):

    class Meta:
        model = Business
        fields = '__all__'



