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
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    coef_first_class = models.DecimalField(max_digits=4, decimal_places=2, default=5.00)
    coef_business_class = models.DecimalField(max_digits=4, decimal_places=2, default=2.50)
    status = models.CharField(
        max_length=20,
        choices=FlightStatus.choices,
        default=FlightStatus.SCHEDULED
    )

    def calculate_seat_price(self, row_number):
        plane_type = self.airplane.model
        
        if row_number <= plane_type.first_class_rows:
            return self.base_price * self.coef_first_class  
        elif row_number <= (plane_type.first_class_rows + plane_type.business_class_rows):
            return self.base_price * self.coef_business_class
        return self.base_price 
    
    def __str__(self):
        return f"{self.flight_number} ({self.route})"