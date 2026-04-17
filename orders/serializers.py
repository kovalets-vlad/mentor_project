from rest_framework import serializers
from .models import Order, Ticket

class TicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ticket
        fields = ('id', 'row', 'seat', 'flight', 'order', 'status')

class OrderSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'user', 'tickets')
        read_only_fields = ('user',)