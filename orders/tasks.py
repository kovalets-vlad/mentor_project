from celery import shared_task
from django.db import transaction

from .models import Order
from .choices import OrderStatus, TicketStatus

@shared_task
def expire_pending_order(order_id):
    with transaction.atomic():
        try:
            order = Order.objects.select_for_update().get(id=order_id)

            if order.status == OrderStatus.PENDING:
                order.status = OrderStatus.EXPIRED
                order.save()
    
                order.tickets.update(status=TicketStatus.CANCELLED)
                
                return f"Order {order_id} has been expired and tickets released."
            
            return f"Order {order_id} is safe (Status: {order.status})."

        except Order.DoesNotExist:
            return f"Order {order_id} does not exist."