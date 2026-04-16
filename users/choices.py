from django.db import models

class UserRole(models.TextChoices):
    CUSTOMER = "customer",
    ADMIN = "admin", 