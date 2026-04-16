from django.contrib.auth.models import AbstractUser
from django.db import models
from .choices import UserRole

class User(AbstractUser):
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.CUSTOMER
    )
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    passport_number = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_staff_member(self):
        return self.role in [UserRole.AIRLINE_STAFF, UserRole.AIRPORT_ADMIN]