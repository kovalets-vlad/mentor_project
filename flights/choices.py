from django.db import models

class FlightStatus(models.TextChoices):
    SCHEDULED = "scheduled", 
    BOARDING = "boarding", 
    DEPARTED = "departed", 
    DELAYED = "delayed", 
    CANCELLED = "cancelled", 
