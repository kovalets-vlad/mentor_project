from django.db import models

class AirplaneType(models.Model):
    name = models.CharField(max_length=255) 
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    @property
    def capacity(self):
        return self.rows * self.seats_in_row

    def __str__(self):
        return self.name

class Airplane(models.Model):
    name = models.CharField(max_length=255) 
    model = models.ForeignKey(AirplaneType, on_delete=models.CASCADE)
    airline = models.ForeignKey('airports.Airline', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name} ({self.model.name})"