from rest_framework import serializers
from .models import Country, Airport, Airline, AirplaneType, Airplane

class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ('id', 'name', 'code')

class AirportSerializer(serializers.ModelSerializer):
    country_name = serializers.CharField(source='country.name', read_only=True)

    class Meta:
        model = Airport
        fields = ('id', 'name', 'city', 'country', 'country_name')

class AirlineSerializer(serializers.ModelSerializer):
    country_name = serializers.CharField(source='country.name', read_only=True)

    class Meta:
        model = Airline
        fields = ('id', 'name', 'iata_code', 'country', 'country_name')

class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ('id', 'name', 'rows', 'seats_in_row', 'capacity')

class AirplaneSerializer(serializers.ModelSerializer):
    airplane_type_name = serializers.CharField(source='airplane_type.name', read_only=True)

    class Meta:
        model = Airplane
        fields = ('id', 'name', 'model', 'airplane_type', 'airplane_type_name', 'airline')