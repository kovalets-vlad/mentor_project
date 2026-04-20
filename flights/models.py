from django.db import models
from django.db.models import Count, Q

from orders.choices import TicketStatus
from airports.models import Airport, Airplane
from core.models import BaseModel
from .choices import FlightStatus
from users.choices import UserRole

class RouteQuerySet(models.QuerySet):
    def visible_for(self, user):
        if user.is_anonymous:
            return self.all() 
        
        if user.is_system_admin or user.role == UserRole.AIRLINE_ADMIN:
            return self.all()

        if user.role == UserRole.AIRPORT_ADMIN and user.managed_airport:
            return self.filter(
                Q(source=user.managed_airport) | Q(destination=user.managed_airport)
            )
        return self.all()

class Route(models.Model):
    source = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='departure_routes')
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='arrival_routes')
    distance = models.IntegerField()

    objects = RouteQuerySet.as_manager()


    def __str__(self):
        return f"{self.source.name} -> {self.destination.name}"
    

class FlightQuerySet(models.QuerySet):
    def visible_for(self, user):

        if user.is_anonymous or user.role == UserRole.CUSTOMER:
            return self.filter(status=FlightStatus.SCHEDULED)
        
        if user.is_system_admin:
            return self
        
        if user.is_airport_manager:
            return self.filter(route__source=user.managed_airport)
            
        if user.is_airline_manager:
            return self.filter(airplane__airline=user.managed_airline)

        return self.none()
    
    def with_details_and_ticket_counts(self):
        return self.select_related(
            'route__source', 'route__destination', 'airplane__model'
        ).annotate(
            active_tickets_count=Count(
                'tickets', 
                filter=~Q(tickets__status=TicketStatus.CANCELLED)
            )
        )

class Flight(BaseModel):
    flight_number = models.CharField(max_length=10, unique=True, null=True) 
    
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='flights')
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE, related_name='flights')
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    coef_first_class = models.DecimalField(max_digits=4, decimal_places=2, default=5.00)
    coef_business_class = models.DecimalField(max_digits=4, decimal_places=2, default=2.50)
    status = models.CharField(
        max_length=20,
        choices=FlightStatus.choices,
        default=FlightStatus.SCHEDULED
    )

    objects = FlightQuerySet.as_manager()

    def calculate_seat_price(self, row_number):
        plane_type = self.airplane.model
        
        if row_number <= plane_type.first_class_rows:
            return self.base_price * self.coef_first_class  
        elif row_number <= (plane_type.first_class_rows + plane_type.business_class_rows):
            return self.base_price * self.coef_business_class
        return self.base_price 
    
    def __str__(self):
        return f"{self.flight_number} ({self.route})"