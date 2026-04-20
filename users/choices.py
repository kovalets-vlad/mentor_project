from django.db import models
from django.utils.translation import gettext_lazy as _

class UserRole(models.TextChoices):
    CUSTOMER = "customer", _("Customer")
    AIRPORT_ADMIN = "airport_admin", _("Airport Admin")
    AIRLINE_ADMIN = "airline_admin", _("Airline Admin") 
    SYSTEM_ADMIN = "system_admin", _("System Admin")