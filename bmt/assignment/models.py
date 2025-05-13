from django.db import models
from django.contrib.auth.models import User

from assignment.choices import ASSIGNMENT_STATUSES
from business.models import Business


class Assignment(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    notes = models.TextField()
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignments_assigned')
    due_date = models.DateField()
    status = models.CharField(max_length=500, choices=ASSIGNMENT_STATUSES)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='assignments_uploaded')

    def __str__(self):
        return self.title

