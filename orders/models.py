from django.db import models
from django.conf import settings
from django.db.models import Q 

from flights.models import Flight
from core.models import BaseModel
from .choices import TicketStatus, OrderStatus

class Order(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)

    def __str__(self):
        return f"Order {self.id} by {self.user.email} - {self.get_status_display()}"


class Ticket(BaseModel):
    row = models.IntegerField()
    seat = models.IntegerField()
    flight = models.ForeignKey(Flight, on_delete=models.CASCADE, related_name='tickets')
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='tickets')

    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    status = models.CharField(
        max_length=20,
        choices=TicketStatus.choices,
        default=TicketStatus.BOOKED
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['row', 'seat', 'flight'],
                condition=~Q(status=TicketStatus.CANCELLED), 
                name='unique_active_seat_per_flight'
            )
        ]

    def __str__(self):
        return f"Ticket {self.id} (Row: {self.row}, Seat: {self.seat}, Status: {self.status})"