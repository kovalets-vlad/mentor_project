from django.db import models

class UserRole(models.TextChoices):
    CUSTOMER = "customer",
    AIRPORT_ADMIN = "airport_admin", 