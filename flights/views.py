from rest_framework import viewsets
from core.filters import RoleBasedFilterBackend
from .permissions import IsFlightManagerOrSuperAdmin
from .models import Route, Flight
from .serializers import RouteSerializer, FlightListSerializer, FlightDetailSerializer, FlightCreateUpdateSerializer

class RouteViewSet(viewsets.ModelViewSet):
    serializer_class = RouteSerializer
    permission_classes = [IsFlightManagerOrSuperAdmin] 
    filter_backends = [RoleBasedFilterBackend]

    def get_queryset(self):
            return Route.objects.all().select_related('source', 'destination')


class FlightViewSet(viewsets.ModelViewSet):
    permission_classes = [IsFlightManagerOrSuperAdmin]
    filter_backends = [RoleBasedFilterBackend]

    def get_queryset(self):
        return Flight.objects.with_details_and_ticket_counts().order_by('departure_time')

    def get_serializer_class(self):
        if self.action == 'list':
            return FlightListSerializer
        
        if self.action == 'retrieve':
            return FlightDetailSerializer
        
        if self.action in ['create', 'update', 'partial_update']:
            return FlightCreateUpdateSerializer
            
        return FlightListSerializer 