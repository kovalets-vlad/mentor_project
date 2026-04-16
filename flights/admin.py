from django.contrib import admin
from .models import Route, Flight

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('source', 'destination', 'distance')

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = ('flight_number', 'route', 'departure_time', 'status')
    list_filter = ('status', 'departure_time')
    search_fields = ('flight_number',)