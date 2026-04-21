from django.contrib import admin
from .models import Order, Ticket

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'total_price', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__email',) 

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('id', 'flight', 'order', 'row', 'seat', 'price', 'status')
    list_filter = ('status', 'flight')
    search_fields = ('order__id',)