from django.db import models

class Country(models.Model):
    name = models.CharField(max_length=255, unique=True)
    code = models.CharField(max_length=5, unique=True, help_text="ISO Country Code")

    class Meta:
        verbose_name_plural = "Countries"

    def __str__(self):
        return f"{self.name} ({self.code})"

class Airline(models.Model):
    name = models.CharField(max_length=255)
    iata_code = models.CharField(max_length=5, unique=True)

    def __str__(self):
        return f"{self.name} [{self.iata_code}]"