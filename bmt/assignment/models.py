from django.db import models
from django.contrib.auth.models import User

class Assignment(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    notes = models.TextField()
    business = models.CharField(max_length=500)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    due_date = models.DateField()
    status = models.CharField(max_length=500)
    uploaded_by = models.CharField(max_length=500)
