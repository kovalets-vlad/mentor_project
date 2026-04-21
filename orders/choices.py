from django.db import models
from django.utils.translation import gettext_lazy as _

class OrderStatus(models.TextChoices):
    PENDING = 'pending', _('Pending')
    PAID = 'paid', _('Paid')
    CANCELLED = 'cancelled', _('Cancelled by User')
    REFUNDED = 'refunded', _('Refunded')
    EXPIRED = 'expired', _('Expired (Timeout)')  
    COMPLETED = 'completed', _('Completed (Flight Done)') 

class TicketStatus(models.TextChoices):
    BOOKED = "booked", _("Booked")
    PAID = "paid", _("Paid")
    CANCELLED = "cancelled", _("Cancelled")
    USED = "used", _("Used")