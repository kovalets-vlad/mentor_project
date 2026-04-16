from django.db import models

class FlightStatus(models.TextChoices):
    SCHEDULED = "scheduled", "Запланований"
    BOARDING = "boarding", "Посадка"
    DEPARTED = "departed", "Вилетів"
    DELAYED = "delayed", "Затриманий"
    CANCELLED = "cancelled", "Відмінений"
