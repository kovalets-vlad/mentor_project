from django.db import models
from django.utils.translation import gettext_lazy as _

class SeatClass(models.TextChoices):
    ECONOMY = 'economy', _('Economy')
    BUSINESS = 'business', _('Business')
    FIRST = 'first', _('First Class')