from rest_framework import serializers
from .models import Order, Ticket, TicketStatus

from rest_framework import serializers
from .models import Order, Ticket, TicketStatus, OrderStatus

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('id', 'row', 'seat', 'flight', 'order', 'status')
        read_only_fields = ('status',) 

    def validate(self, attrs):
        order = attrs.get('order', getattr(self.instance, 'order', None))
        flight = attrs.get('flight', getattr(self.instance, 'flight', None))
        row = attrs.get('row', getattr(self.instance, 'row', None))
        seat = attrs.get('seat', getattr(self.instance, 'seat', None))

        if order and order.status != OrderStatus.PENDING:
            raise serializers.ValidationError({
                "order": f"Cannot add or modify tickets in an order that is {order.status}."
            })

        if flight and row and seat:
            model = flight.airplane.model
            max_rows = model.rows
            max_seats_in_row = model.seats_in_row

            if row < 1 or row > max_rows:
                raise serializers.ValidationError({
                    "row": f"This aircraft has only {max_rows} rows. Row {row} does not exist!"
                })

            if seat < 1 or seat > max_seats_in_row:
                raise serializers.ValidationError({
                    "seat": f"Each row has only {max_seats_in_row} seats. Seat {seat} does not exist."
                })

            active_tickets = Ticket.objects.filter(
                flight=flight,
                row=row,
                seat=seat
            ).exclude(status=TicketStatus.CANCELLED)
            
            if self.instance:
                active_tickets = active_tickets.exclude(id=self.instance.id)

            if active_tickets.exists():
                raise serializers.ValidationError(
                    {"seat": f"Seat {row}-{seat} is already booked!"}
                )
            
        return attrs

class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'status', 'created_at', 'tickets')
        read_only_fields = ('user', 'status', 'created_at')