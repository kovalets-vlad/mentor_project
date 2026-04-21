from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from orders.models import Order, OrderStatus, TicketStatus

class Command(BaseCommand):
    help = 'Cancels pending orders that are older than 15 minutes and frees up tickets.'

    def handle(self, *args, **kwargs):
        expiration_time = timezone.now() - timedelta(minutes=15)

        expired_orders = Order.objects.filter(
            status=OrderStatus.PENDING, 
            created_at__lt=expiration_time
        )

        count = expired_orders.count()

        if count == 0:
            self.stdout.write(self.style.SUCCESS('No expired orders found. Everything is clean!'))
            return

        for order in expired_orders:
            order.status = OrderStatus.EXPIRED
            order.save()
            
            order.tickets.update(status=TicketStatus.CANCELLED)

        self.stdout.write(self.style.SUCCESS(f'Successfully cancelled {count} expired orders.'))