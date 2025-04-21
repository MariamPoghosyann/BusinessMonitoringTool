from django.contrib.auth.models import User
from django.db import models

class Report(models.Model):
    record_id = models.CharField(max_length=255)
    business = models.CharField(max_length=255)
    plan_fact = models.CharField(max_length=255)
    date = models.DateField()
    parent_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    show = models.BooleanField(default=True)
    type = models.CharField(max_length=255)
    operation = models.CharField(max_length=100, null=True, blank=True)
    color_code = models.BooleanField(max_length=255)
    reverse_sign = models.BooleanField()
    value = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)


    #uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)


