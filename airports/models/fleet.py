from django.db import models
from django.db.models import Q

class AirplaneTypeQuerySet(models.QuerySet):
    def visible_for(self, user):
        if not user.is_authenticated or getattr(user, 'role', 'customer') == 'customer':
            return self.filter(airline__isnull=True)
            
        if user.is_system_admin:
            return self.all()
            
        if user.is_airline_manager:
            return self.filter(Q(airline__isnull=True) | Q(airline=user.managed_airline))
            
        return self.filter(airline__isnull=True)

class AirplaneQuerySet(models.QuerySet):
    def visible_for(self, user):
        if user.is_system_admin:
            return self.all()
            
        if getattr(user, 'is_airline_manager', False):
            return self.filter(airline=user.managed_airline)
            
        return self.none()

class AirplaneType(models.Model):
    name = models.CharField(max_length=255) 
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    airline = models.ForeignKey(
        'airports.Airline', 
        on_delete=models.CASCADE, 
        null=True, blank=True, 
        related_name='custom_airplane_types'
    )

    business_class_rows = models.IntegerField(default=0, help_text="Number of rows starting from the front")
    first_class_rows = models.IntegerField(default=0)

    objects = AirplaneTypeQuerySet.as_manager()

    @property
    def capacity(self):
        return self.rows * self.seats_in_row

    def __str__(self):
        return self.name

class Airplane(models.Model):
    name = models.CharField(max_length=255) 
    model = models.ForeignKey(AirplaneType, on_delete=models.CASCADE)
    airline = models.ForeignKey('airports.Airline', on_delete=models.CASCADE)

    objects = AirplaneQuerySet.as_manager()

    def __str__(self):
        return f"{self.name} ({self.model.name})"