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
        instance = self.instance
        source = attrs.get('source', getattr(instance, 'source', None))
        destination = attrs.get('destination', getattr(instance, 'destination', None))
        distance = attrs.get('distance', getattr(instance, 'distance', None))
        
        user = self.context.get('request').user

        if user.is_airport_manager:
            if source and source != user.managed_airport:
                raise serializers.ValidationError(
                    {"source": "You can only create routes departing from your assigned airport."}
                )

        if source and destination and source == destination:
            raise serializers.ValidationError(
                {"destination": "The arrival airport cannot be the same as the departure airport!"}
            )
            
        if distance is not None and distance <= 0:
            raise serializers.ValidationError(
                {"distance": "Distance must be strictly greater than 0."}
            )
            
        return attrs

class FlightBaseSerializer(serializers.ModelSerializer):
    route_details = serializers.StringRelatedField(source='route', read_only=True)
    airplane_name = serializers.CharField(source='airplane.name', read_only=True)

    class Meta:
        model = Flight
        fields = ('id', 'flight_number', 'departure_time', 'arrival_time', 'status')


class FlightListSerializer(FlightBaseSerializer):
    class Meta(FlightBaseSerializer.Meta):
        fields = FlightBaseSerializer.Meta.fields + ('route_details', 'airplane_name')


class FlightDetailSerializer(FlightBaseSerializer):
    available_seats = serializers.SerializerMethodField()
    price_business = serializers.SerializerMethodField()
    price_first = serializers.SerializerMethodField()

    total_seats = serializers.IntegerField(source='airplane.model.capacity', read_only=True)

    class Meta(FlightBaseSerializer.Meta):
        fields = FlightBaseSerializer.Meta.fields + (
            'route', 'airplane', 'route_details', 'airplane_name',
            'total_seats', 'available_seats', 'base_price', 
            'price_business', 'price_first'
        )
    def get_available_seats(self, obj):
        total = obj.airplane.model.capacity 
        active_tickets = getattr(obj, 'active_tickets_count', 0)
        return max(0, total - active_tickets) 

    def _calculate_class_price(self, base_price, coef):
        """Helper to calculate price with decimal precision"""
        if not base_price:
            return None
        return round(base_price * Decimal(str(coef)), 2)

    def get_price_business(self, obj):
        return self._calculate_class_price(obj.base_price, obj.coef_business_class)

    def get_price_first(self, obj):
        return self._calculate_class_price(obj.base_price, obj.coef_first_class)


class FlightCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Flight
        fields = '__all__'

    def validate(self, attrs):
        instance = self.instance
        user = self.context.get('request').user
        
        departure_time = attrs.get('departure_time', getattr(instance, 'departure_time', None))
        arrival_time = attrs.get('arrival_time', getattr(instance, 'arrival_time', None))
        airplane = attrs.get('airplane', getattr(instance, 'airplane', None))
        route = attrs.get('route', getattr(instance, 'route', None))
        base_price = attrs.get('base_price', getattr(instance, 'base_price', None))

        if user.is_airport_manager and route:
            if route.source != user.managed_airport:
                raise serializers.ValidationError({"route": "You can only manage flights from your assigned airport."})

        if user.is_airline_manager and airplane:
            if airplane.airline != user.managed_airline:
                raise serializers.ValidationError({"airplane": "This plane does not belong to your airline."})
        
        if not instance and departure_time and departure_time < timezone.now():
            raise serializers.ValidationError({"departure_time": "Departure cannot be scheduled in the past!"})
        
        if arrival_time and departure_time and arrival_time <= departure_time:
            raise serializers.ValidationError({"arrival_time": "Arrival time must be later than departure time!"})

        if base_price is not None and base_price <= 0:
            raise serializers.ValidationError({"base_price": "Base price must be greater than 0."})

        if airplane and departure_time and arrival_time:
            overlaps = Flight.objects.filter(
                airplane=airplane,
                departure_time__lt=arrival_time,
                arrival_time__gt=departure_time
            )
            if instance:
                overlaps = overlaps.exclude(pk=instance.pk)

            if overlaps.exists():
                raise serializers.ValidationError({"airplane": "This airplane is already booked for another flight at this time!"})
            
        return attrs