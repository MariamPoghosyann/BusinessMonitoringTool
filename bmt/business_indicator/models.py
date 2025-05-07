from django.contrib.auth.models import User
from django.db import models
from business.models import Business
from business_indicator.choices import ShowChoices

class Report(models.Model):
    record_id = models.CharField(max_length=255)
    business = models.ForeignKey(Business, on_delete=models.CASCADE)
    plan_fact = models.CharField(max_length=255)
    date = models.DateField()
    parent_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    show = models.CharField(max_length=3, choices=ShowChoices.choices, default=ShowChoices.NO)
    type = models.CharField(max_length=255)
    operation = models.CharField(max_length=100, null=True, blank=True)
    color_code = models.BooleanField(max_length=255)
    reverse_sign = models.BooleanField()
    value = models.DecimalField(max_digits=20, decimal_places=2, null=True, blank=True)


    def __str__(self):
        return self.name

class Deviation(models.Model):
    class Meta:
        managed = False




