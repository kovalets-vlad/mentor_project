from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwnerOrAdmin 
from .models import Order, Ticket
from .serializers import OrderSerializer, TicketSerializer
from users.choices import UserRole

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin] 

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.role == UserRole.ADMIN:
            return Order.objects.all().prefetch_related('tickets')
        return Order.objects.filter(user=self.request.user).prefetch_related('tickets')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.role == UserRole.ADMIN:
            return Ticket.objects.all().select_related('flight', 'order')
        return Ticket.objects.filter(order__user=self.request.user).select_related('flight', 'order')