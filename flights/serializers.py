from rest_framework import serializers
from django.utils import timezone

from .models import Route, Flight
from orders.choices import TicketStatus

class RouteSerializer(serializers.ModelSerializer):
    source_code = serializers.CharField(source='source.iata_code', read_only=True)
    destination_code = serializers.CharField(source='destination.iata_code', read_only=True)

    class Meta:
        model = Route
        fields = ('id', 'source', 'source_code', 'destination', 'destination_code', 'distance')

    def validate(self, attrs):
        if attrs.get('source') == attrs.get('destination'):
            raise serializers.ValidationError(
                {"destination": "The arrival airport cannot be the same as the departure airport!"}
            )
        return attrs

from rest_framework import serializers
from .models import Flight
from django.utils import timezone

class FlightSerializer(serializers.ModelSerializer):
    route_details = serializers.StringRelatedField(source='route', read_only=True)
    airplane_name = serializers.CharField(source='airplane.name', read_only=True)
    
    total_seats = serializers.IntegerField(
        source='airplane.model.capacity', 
        read_only=True
    )
    available_seats = serializers.SerializerMethodField()

    class Meta:
        model = Flight
        fields = (
            'id', 'flight_number', 'route', 'route_details', 
            'airplane', 'airplane_name', 'departure_time', 
            'arrival_time', 'status', 'total_seats', 'available_seats'
        )

    def get_available_seats(self, obj):
        total = obj.airplane.model.capacity 
        active_tickets = getattr(obj, 'active_tickets_count', 0)
        
        return total - active_tickets

    def validate(self, attrs):
        departure_time = attrs.get('departure_time')
        arrival_time = attrs.get('arrival_time')
        airplane = attrs.get('airplane')

        if not self.instance and departure_time < timezone.now():
            raise serializers.ValidationError(
                {"departure_time": "Departure cannot be scheduled in the past tense!"}
            )
        
        if arrival_time <= departure_time:
            raise serializers.ValidationError(
                {"arrival_time": "Arrival time must be later than departure time!"}
            )

        overlapping_flights = Flight.objects.filter(
            airplane=airplane,
            departure_time__lt=arrival_time,  
            arrival_time__gt=departure_time   
        )

        if self.instance:
            overlapping_flights = overlapping_flights.exclude(pk=self.instance.pk)

        if overlapping_flights.exists():
            raise serializers.ValidationError(
                {"airplane": "This plane is already occupied by another flight during this time period!"}
            )

        return attrs