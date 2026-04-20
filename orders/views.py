from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets
from django.utils import timezone
from datetime import timedelta
from django.db import transaction

from users.choices import UserRole
from .permissions import IsOwnerOrAdmin 
from .models import Order, Ticket
from .serializers import OrderSerializer, TicketSerializer
from .choices import OrderStatus, TicketStatus

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
        with transaction.atomic():
            try:
                order = Order.objects.select_for_update().get(pk=pk)
                
                if order.status != OrderStatus.PENDING:
                    return Response(
                        {"detail": "This order has already been processed or canceled."}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )

                order.status = OrderStatus.PAID
                order.save()

                order.tickets.update(status=TicketStatus.PAID)

            except Order.DoesNotExist:
                return Response(
                    {"detail": "Order not found."}, 
                    status=status.HTTP_404_NOT_FOUND
                )
            except Exception as e:
                return Response(
                    {"detail": f"An error occurred during payment processing: {str(e)}"}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(
            {"detail": "Successfully paid! All tickets secured."}, 
            status=status.HTTP_200_OK
        )

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        """
        Cancels a pending order and releases associated tickets.
        Ensures that both order and tickets are updated together.
        """
        with transaction.atomic():
            try:
                order = Order.objects.select_for_update().get(pk=pk)

                if order.status != OrderStatus.PENDING:
                    return Response(
                        {"detail": "Only pending orders can be canceled."}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )

                order.status = OrderStatus.CANCELLED
                order.save()

                order.tickets.update(status=TicketStatus.CANCELLED)

            except Order.DoesNotExist:
                return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response(
                    {"detail": f"An error occurred during cancellation: {str(e)}"}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response({"detail": "Order canceled and seats released."}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def refund(self, request, pk=None):
        """
        Refunds a paid order. Checks time constraints and updates status.
        Uses atomic transaction to ensure financial consistency.
        """
        MAGIC_HOURS = 3 
        
        with transaction.atomic():
            try:
                order = Order.objects.select_for_update().get(pk=pk)

                if order.status != OrderStatus.PAID:
                    return Response(
                        {"detail": "Only paid orders can be refunded."}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )

                first_ticket = order.tickets.select_related('flight').first()
                if not first_ticket:
                    return Response({"detail": "No tickets found."}, status=status.HTTP_404_NOT_FOUND)

                flight_departure = first_ticket.flight.departure_time
                if timezone.now() > flight_departure - timedelta(hours=MAGIC_HOURS):
                    return Response(
                        {"detail": f"Too late for a refund. Less than {MAGIC_HOURS} hours before flight."}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )
                
                order.status = OrderStatus.REFUNDED
                order.save()

                order.tickets.update(status=TicketStatus.CANCELLED)

            except Order.DoesNotExist:
                return Response({"detail": "Order not found."}, status=status.HTTP_404_NOT_FOUND)
            except Exception as e:
                return Response(
                    {"detail": f"Refund failed: {str(e)}"}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response({"detail": "Refund processed successfully."}, status=status.HTTP_200_OK)


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