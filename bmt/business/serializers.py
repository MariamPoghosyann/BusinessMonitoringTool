from rest_framework import serializers
from .models import Business
class AssignmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = '__all__'