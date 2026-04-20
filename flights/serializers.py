from rest_framework import serializers
from django.utils import timezone
from decimal import Decimal

from .models import Route, Flight

class RouteSerializer(serializers.ModelSerializer):
    source_code = serializers.CharField(source='source.iata_code', read_only=True)
    destination_code = serializers.CharField(source='destination.iata_code', read_only=True)

    class Meta:
        model = Route
        fields = ('id', 'source', 'source_code', 'destination', 'destination_code', 'distance')

    def validate(self, attrs):
        source = attrs.get('source', getattr(self.instance, 'source', None))
        destination = attrs.get('destination', getattr(self.instance, 'destination', None))
        distance = attrs.get('distance', getattr(self.instance, 'distance', None))

        if source and destination and source == destination:
            raise serializers.ValidationError(
                {"destination": "The arrival airport cannot be the same as the departure airport!"}
            )
            
        if distance is not None and distance <= 0:
            raise serializers.ValidationError(
                {"distance": "Distance must be strictly greater than 0."}
            )
            
        return attrs

class FlightSerializer(serializers.ModelSerializer):
    route_details = serializers.StringRelatedField(source='route', read_only=True)
    airplane_name = serializers.CharField(source='airplane.name', read_only=True)
    
    total_seats = serializers.IntegerField(
        source='airplane.model.capacity', 
        read_only=True
    )
    available_seats = serializers.SerializerMethodField()
    
    price_business = serializers.SerializerMethodField()
    price_first = serializers.SerializerMethodField()

    class Meta:
        model = Flight
        fields = (
            'id', 'flight_number', 'route', 'route_details', 
            'airplane', 'airplane_name', 'departure_time', 
            'arrival_time', 'status', 'total_seats', 'available_seats',
            'base_price', 'price_business', 'price_first' 
        )

    def get_available_seats(self, obj):
        total = obj.airplane.model.capacity 
        active_tickets = getattr(obj, 'active_tickets_count', 0)
        return total - active_tickets

    def get_price_business(self, obj):
        if not obj.base_price:
            return None
            
        coef = Decimal(str(obj.coef_business_class))
        return round(obj.base_price * coef, 2)

    def get_price_first(self, obj):
        if not obj.base_price:
            return None
            
        coef = Decimal(str(obj.coef_first_class))
        return round(obj.base_price * coef, 2)
    
    def validate(self, attrs):
        departure_time = attrs.get('departure_time', getattr(self.instance, 'departure_time', None))
        arrival_time = attrs.get('arrival_time', getattr(self.instance, 'arrival_time', None))
        airplane = attrs.get('airplane', getattr(self.instance, 'airplane', None))
        base_price = attrs.get('base_price', getattr(self.instance, 'base_price', None))
        
        if not self.instance and departure_time and departure_time < timezone.now():
            raise serializers.ValidationError(
                {"departure_time": "Departure cannot be scheduled in the past!"}
            )
        
        if arrival_time and departure_time and arrival_time <= departure_time:
            raise serializers.ValidationError(
                {"arrival_time": "Arrival time must be later than departure time!"}
            )

        if base_price is not None and base_price <= 0:
            raise serializers.ValidationError(
                {"base_price": "Base price must be strictly greater than 0."}
            )

        if airplane and departure_time and arrival_time:
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