from rest_framework import serializers
from .models import Route, Flight

class RouteSerializer(serializers.ModelSerializer):
    source_code = serializers.CharField(source='source.iata_code', read_only=True)
    destination_code = serializers.CharField(source='destination.iata_code', read_only=True)

    class Meta:
        model = Route
        fields = ('id', 'source', 'source_code', 'destination', 'destination_code', 'distance')

    def validate(self, attrs):
        if attrs.get('source') == attrs.get('destination'):
            raise serializers.ValidationError(
                {"destination": "Аеропорт прильоту не може співпадати з аеропортом вильоту!"}
            )
        return attrs

class FlightSerializer(serializers.ModelSerializer):
    route_details = serializers.StringRelatedField(source='route', read_only=True)
    airplane_name = serializers.CharField(source='airplane.name', read_only=True)

    class Meta:
        model = Flight
        fields = (
            'id', 'flight_number', 'route', 'route_details', 
            'airplane', 'airplane_name', 'departure_time', 
            'arrival_time', 'status'
        )

    def validate(self, attrs):
        if attrs.get('arrival_time') <= attrs.get('departure_time'):
            raise serializers.ValidationError(
                {"arrival_time": "Час прильоту має бути пізнішим за час вильоту!"}
            )
        return attrs