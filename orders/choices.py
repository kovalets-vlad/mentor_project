from django.db import models

class TicketStatus(models.TextChoices):
    BOOKED = "booked", 
    PAID = "paid", 
    CANCELLED = "cancelled", 
    USED = "used", 