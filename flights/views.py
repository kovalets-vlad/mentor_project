from rest_framework import viewsets
from django.db.models import Count, Q

from core.permissions import IsAdminOrReadOnly
from orders.choices import TicketStatus
from .models import Route, Flight
from .serializers import RouteSerializer, FlightSerializer



class RouteViewSet(viewsets.ModelViewSet):
    queryset = Route.objects.all().select_related('source', 'destination')
    serializer_class = RouteSerializer
    permission_classes = [IsAdminOrReadOnly]


class FlightViewSet(viewsets.ModelViewSet):
    serializer_class = FlightSerializer
    permission_classes = [IsAdminOrReadOnly] 

    def get_queryset(self):
        return Flight.objects.select_related(
            'route__source', 'route__destination', 'airplane__model'
        ).annotate(
            active_tickets_count=Count(
                'tickets', 
                filter=~Q(tickets__status=TicketStatus.CANCELLED)
            )
        )