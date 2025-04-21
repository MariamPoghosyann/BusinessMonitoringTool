from django.db import models
from django.contrib.auth.models import User

class Business(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    responsible_person = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

# Create your models here.
