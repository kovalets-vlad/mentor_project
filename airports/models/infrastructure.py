from django.db import models
from .base import Country

class Airport(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name="airports")

    def __str__(self):
        return f"{self.name}"