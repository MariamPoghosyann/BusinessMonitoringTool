from rest_framework import serializers
from .models import Reports

class ReportsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reports
        fields = '__all__'

class CSVUploaderSerializer(serializers.Serializer):
    file = serializers.FileField()




