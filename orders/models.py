from django.db import models
from django.conf import settings
from django.db.models import Q, Sum

from flights.models import Flight
from core.models import BaseModel
from .choices import TicketStatus, OrderStatus

class OrderQuerySet(models.QuerySet):
    def visible_for(self, user):
        if user.is_system_admin:
            return self.all()
            
        if user.is_authenticated:
            return self.filter(user=user)
            
        return self.none()

class TicketQuerySet(models.QuerySet):
    def visible_for(self, user):
        if user.is_system_admin:
            return self.all()
            
        if user.is_authenticated:
            customer_filter = Q(order__user=user)
            
            if getattr(user, 'is_airline_manager', False):
                airline_filter = Q(flight__airplane__airline=user.managed_airline)
                return self.filter(customer_filter | airline_filter)
                
            return self.filter(customer_filter)
            
        return self.none()

class Order(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    status = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)

    objects = OrderQuerySet.as_manager()

    @property
    def total_price(self):
        result = self.tickets.exclude(status=TicketStatus.CANCELLED).aggregate(total=Sum('price'))
        return result['total'] or 0.00

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

    objects = TicketQuerySet.as_manager()

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