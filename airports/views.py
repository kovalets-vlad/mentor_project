from rest_framework import viewsets, generics
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Country, Airport, Airline, AirplaneType, Airplane
from .serializers import (
    CountrySerializer, AirportSerializer, 
    AirplaneTypeSerializer, AirplaneSerializer,
    AirlineSerializer
)
from core.filters import RoleBasedFilterBackend 
from core.permissions import IsSystemAdminOrReadOnly, IsAirlineManagerOrSuperAdmin

class CountryListCreateView(generics.ListCreateAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsSystemAdminOrReadOnly]

class CountryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = [IsSystemAdminOrReadOnly]

class AirportViewSet(viewsets.ModelViewSet):
    queryset = Airport.objects.all()
    serializer_class = AirportSerializer
    permission_classes = [IsSystemAdminOrReadOnly]

    @action(detail=False, methods=['get'])
    def cities(self, request):
        cities = Airport.objects.values_list('city', flat=True).distinct().order_by('city')
        
        valid_cities = [city for city in cities if city]
        
        return Response(valid_cities)

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