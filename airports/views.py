from rest_framework import viewsets
from .models import Country, Airport, Airline, AirplaneType, Airplane
from .serializers import (
    CountrySerializer, AirportSerializer, 
    AirplaneTypeSerializer, AirplaneSerializer,
    AirlineSerializer
)
from core.filters import RoleBasedFilterBackend 
from core.permissions import IsSystemAdminOrReadOnly

class CountryViewSet(viewsets.ModelViewSet):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsSystemAdminOrReadOnly] 

class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = [IsSystemAdminOrReadOnly]

class AirlineViewSet(viewsets.ModelViewSet):
    queryset = Airline.objects.all()
    serializer_class = AirlineSerializer
    permission_classes = [IsSystemAdminOrReadOnly]

class AirplaneTypeViewSet(viewsets.ModelViewSet):
    serializer_class = AirplaneTypeSerializer
    filter_backends = [RoleBasedFilterBackend]
    permission_classes = [IsAirlineManagerOrSuperAdmin] 

    def get_queryset(self):
        return AirplaneType.objects.all()
    
class AirplaneViewSet(viewsets.ModelViewSet):
    serializer_class = AirplaneSerializer
    filter_backends = [RoleBasedFilterBackend]
    permission_classes = [IsAirlineManagerOrSuperAdmin]

    def get_queryset(self):
        return Airplane.objects.all().select_related('model', 'airline')