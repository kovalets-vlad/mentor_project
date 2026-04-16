from django.db import models

class UserRole(models.TextChoices):
    CUSTOMER = "customer", "Пасажир"
    AIRPORT_ADMIN = "airport_admin", "Адміністратор аеропорту"