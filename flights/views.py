from rest_framework import viewsets
from .models import Route, Flight
from .serializers import RouteSerializer, FlightSerializer
from core.permissions import IsAdminOrReadOnly

class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all().select_related('source', 'destination')
    serializer_class = RouteSerializer
    permission_classes = [IsAdminOrReadOnly]

class FlightViewSet(viewsets.ModelViewSet):
    queryset = Flight.objects.all().select_related(
        'route__source', 'route__destination', 'airplane'
    )
    serializer_class = FlightSerializer
    permission_classes = [IsAdminOrReadOnly]