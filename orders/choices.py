from django.db import models

class TicketStatus(models.TextChoices):
    BOOKED = "booked", "Заброньований"
    PAID = "paid", "Оплачений"
    CANCELLED = "cancelled", "Скасований"
    USED = "used", "Використаний"