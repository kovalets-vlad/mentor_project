from django.db import models
from airports.models import Airport, Airplane
from core.models import BaseModel
from .choices import FlightStatus

class Route(models.Model):
    source = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='departure_routes')
    destination = models.ForeignKey(Airport, on_delete=models.CASCADE, related_name='arrival_routes')
    distance = models.IntegerField()

    def __str__(self):
        return f"{self.source.name} -> {self.destination.name}"

class Flight(BaseModel):
    flight_number = models.CharField(max_length=10, unique=True, null=True) 
    
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name='flights')
    airplane = models.ForeignKey(Airplane, on_delete=models.CASCADE, related_name='flights')
    departure_time = models.DateTimeField()
    arrival_time = models.DateTimeField()
    status = models.CharField(
        max_length=20,
        choices=FlightStatus.choices,
        default=FlightStatus.SCHEDULED
    )

    def __str__(self):
        return f"{self.flight_number} ({self.route})"