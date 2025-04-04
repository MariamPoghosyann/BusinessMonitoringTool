from django.db import models
from django.contrib.auth.models import User
from .choices import ASSIGNMENT_STATUSES

class Assignment(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    notes = models.TextField()
    business = models.CharField(max_length=500)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE)
    due_date = models.DateField()
    status = models.CharField(max_length=500, choices=ASSIGNMENT_STATUSES)
    uploaded_by = models.CharField(max_length=500)

    def __str__(self):
        return self.title