from django.db import models
from django.conf import settings

from flights.models import Flight
from core.models import BaseModel
from .choices import TicketStatus

class Order(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')

    def __str__(self):
        return f"Order {self.id} by {self.user.email}"

class Ticket(BaseModel):
    row = models.IntegerField()
    seat = models.IntegerField()
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='tickets')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='tickets')
    status = models.CharField(
        max_length=20,
        choices=TicketStatus.choices,
        default=TicketStatus.BOOKED
    )

    class Meta:
        unique_together = ('row', 'seat', 'flight')

    def __str__(self):
        return f"Ticket {self.id} (Row: {self.row}, Seat: {self.seat}, Status: {self.status})"