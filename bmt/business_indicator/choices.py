from django.db import models


class ShowChoices(models.TextChoices):
    YES = "YES", "yes",
    NO = "NO", "no"

