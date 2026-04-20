from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.utils import timezone
from datetime import timedelta

from users.choices import UserRole
from .permissions import IsOwnerOrAdmin 
from .models import Order, Ticket
from .serializers import OrderSerializer, TicketSerializer
from .choices import OrderStatus, TicketStatus

MAGIC_HOURS = 3


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin] 

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.role == UserRole.ADMIN:
            return Order.objects.all().prefetch_related('tickets')
        return Order.objects.filter(user=self.request.user).prefetch_related('tickets')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def pay(self, request, pk=None):
        order = self.get_object()

        if order.status != OrderStatus.PENDING:
            return Response({"detail": "This order has already been processed or canceled."}, status=status.HTTP_400_BAD_REQUEST)

        order.status = OrderStatus.PAID
        order.save()

        order.tickets.update(status=TicketStatus.PAID)

        return Response({"detail": "Successfully paid!"}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()

        if order.status != OrderStatus.PENDING:
            return Response({"detail": "You can only cancel pending orders."}, status=status.HTTP_400_BAD_REQUEST)

        order.status = OrderStatus.CANCELLED
        order.save()

        order.tickets.update(status=TicketStatus.CANCELLED)

        return Response({"detail": "The order has been canceled, the seats are free again."}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['post'])
    def refund(self, request, pk=None):
        order = self.get_object()

        if order.status != OrderStatus.PAID:
            return Response(
                {"detail": "You can only get a refund for a paid order."},
                status=status.HTTP_400_BAD_REQUEST
            )

        first_ticket = order.tickets.select_related('flight').first()
        if not first_ticket:
            return Response({"detail": "No tickets found."}, status=status.HTTP_404_NOT_FOUND)

        flight_departure = first_ticket.flight.departure_time
        
        if timezone.now() > flight_departure - timedelta(hours=MAGIC_HOURS):
            return Response(
                {"detail": f"Too late to return. Less than {MAGIC_HOURS} hours until departure."},
                status=status.HTTP_400_BAD_REQUEST
            )

        #TO DO:
        #Refund implementation

        order.status = OrderStatus.REFUNDED
        order.save()

        order.tickets.update(status=TicketStatus.CANCELLED)

        return Response(
            {"detail": "The money has been refunded, the order has been canceled, and the seats are free again!"},
            status=status.HTTP_200_OK
        )


class TicketViewSet(viewsets.ModelViewSet):
    serializer_class = TicketSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        if self.request.user.is_staff or self.request.user.role == UserRole.ADMIN:
            return Ticket.objects.all().select_related('flight', 'order')
        return Ticket.objects.filter(order__user=self.request.user).select_related('flight', 'order')
    
    def destroy(self, request, *args, **kwargs):
        ticket = self.get_object()

        if ticket.order.status != OrderStatus.PENDING:
            return Response(
                {"detail": f"Cannot remove ticket. The associated order is already {ticket.order.status}."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return super().destroy(request, *args, **kwargs)