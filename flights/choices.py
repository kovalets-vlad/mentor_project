from django.db import models
from django.utils.translation import gettext_lazy as _

class FlightStatus(models.TextChoices):
    SCHEDULED = "scheduled", _("Scheduled")
    BOARDING = "boarding", _("Boarding")
    DEPARTED = "departed", _("Departed")
    DELAYED = "delayed", _("Delayed")
    CANCELLED = "cancelled", _("Cancelled")

