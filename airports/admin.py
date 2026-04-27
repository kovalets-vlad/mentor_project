from django.contrib import admin
from .models import Country, Airport, Airline, AirplaneType, Airplane

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')

@admin.register(AirplaneType)
class AirplaneTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'airline', 'rows', 'seats_in_row', 'capacity')
    list_filter = ('airline',)
    search_fields = ('name',)

@admin.register(Airport)
class AirportAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'country')
    search_fields = ('name', 'city') 
    list_filter = ('country',)

@admin.register(Airline)
class AirlineAdmin(admin.ModelAdmin):
    list_display = ('name', 'iata_code')
    search_fields = ('name', 'iata_code')

@admin.register(Airplane)
class AirplaneAdmin(admin.ModelAdmin):
    list_display = ('name', 'model', 'airline')
    list_filter = ('airline', 'model')
    search_fields = ('name',)