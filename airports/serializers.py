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
    class Meta:
        model = Airline
        fields = ('id', 'name', 'iata_code')

class AirplaneTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AirplaneType
        fields = ('id', 'name', 'rows', 'seats_in_row', 'business_class_rows', 'first_class_rows', 'capacity', 'airline')

    def validate(self, attrs):
        instance = self.instance
        rows = attrs.get('rows', getattr(instance, 'rows', 0))
        seats_in_row = attrs.get('seats_in_row', getattr(instance, 'seats_in_row', 0))
        business_class_rows = attrs.get('business_class_rows', getattr(instance, 'business_class_rows', 0))
        first_class_rows = attrs.get('first_class_rows', getattr(instance, 'first_class_rows', 0))
        airline = attrs.get('airline', getattr(instance, 'airline', None))

        user = self.context.get('request').user

        if user.is_airline_manager:
             if airline and airline != user.managed_airline:
                  raise serializers.ValidationError({"airline": "You can only create airplane types for your own airline."})

        if rows <= 0:
            raise serializers.ValidationError({"rows": "An airplane must have at least 1 row."})
        if seats_in_row <= 0:
            raise serializers.ValidationError({"seats_in_row": "A row must have at least 1 seat."})

        if (business_class_rows + first_class_rows) > rows:
             raise serializers.ValidationError(
                 {"non_field_errors": "The sum of first class and business class rows cannot exceed total rows."}
             )

        return attrs

class AirplaneSerializer(serializers.ModelSerializer):
    airplane_type_name = serializers.CharField(source='model.name', read_only=True)

    class Meta:
        model = Airplane
        fields = ('id', 'name', 'model', 'airplane_type_name', 'airline')

    def validate(self, attrs):
        instance = self.instance
        user = self.context.get('request').user
        
        airline = attrs.get('airline', getattr(instance, 'airline', None))
        model = attrs.get('model', getattr(instance, 'model', None))

        if user.is_airline_manager:
            if airline and airline != user.managed_airline:
                raise serializers.ValidationError({"airline": "You can only assign planes to your own airline."})
            
            if model and model.airline and model.airline != user.managed_airline:
                raise serializers.ValidationError({"model": "You cannot use a custom airplane type that belongs to another airline."})

        return attrs