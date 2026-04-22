from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend

from core.filters import RoleBasedFilterBackend
from .permissions import IsFlightManagerOrSuperAdmin
from .models import Route, Flight
from .serializers import RouteSerializer, FlightListSerializer, FlightDetailSerializer, FlightCreateUpdateSerializer
from .filters import FlightFilter 

class RouteViewSet(viewsets.ModelViewSet):
    serializer_class = RouteSerializer
    permission_classes = [IsFlightManagerOrSuperAdmin] 
    filter_backends = [RoleBasedFilterBackend]

    def get_queryset(self):
        return Route.objects.all().select_related('source', 'destination')


class FlightViewSet(viewsets.ModelViewSet):
    permission_classes = [IsFlightManagerOrSuperAdmin]
    
    filter_backends = [
        RoleBasedFilterBackend,   
        DjangoFilterBackend,      
        filters.SearchFilter,     
        filters.OrderingFilter    
    ]

    filterset_class = FlightFilter
    search_fields = ['flight_number', 'route__source__city', 'route__destination__city']
    ordering_fields = ['departure_time', 'base_price']

    def get_queryset(self):
        return Flight.objects.with_details_and_ticket_counts()

    def get_serializer_class(self):
        if self.action == 'list':
            return FlightListSerializer
        
        if self.action == 'retrieve':
            return FlightDetailSerializer
        
        if self.action in ['create', 'update', 'partial_update']:
            return FlightCreateUpdateSerializer
            
        return FlightListSerializer