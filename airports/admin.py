from django.contrib import admin
from .models import Country, Airport, Airline, AirplaneType, Airplane

admin.site.register(Country)
admin.site.register(AirplaneType)

@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'country')
    search_fields = ('name', 'city') 
    list_filter = ('country',)

@admin.register(Airline)
class AirlineAdmin(admin.ModelAdmin):
    list_display = ('name', 'iata_code')

@admin.register(Airplane)
class AirplaneAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'airline')
    list_filter = ('airline', 'model')