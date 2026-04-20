from django.db import models

class AirplaneType(models.Model):
    name = models.CharField(max_length=255) 
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    business_class_rows = models.IntegerField(default=0, help_text="Number of rows starting from the front")
    first_class_rows = models.IntegerField(default=0)

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