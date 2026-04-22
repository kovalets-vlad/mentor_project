import django_filters
import django_filters
from .models import Flight
from .choices import FlightStatus

class FlightFilter(django_filters.FilterSet):
    source_id = django_filters.NumberFilter(field_name='route__source_id')
    destination_id = django_filters.NumberFilter(field_name='route__destination_id')
    
    source_city = django_filters.CharFilter(field_name='route__source__city', lookup_expr='icontains')
    destination_city = django_filters.CharFilter(field_name='route__destination__city', lookup_expr='icontains')
    
    date = django_filters.DateFilter(field_name='departure_time', lookup_expr='date')
    
    min_price = django_filters.NumberFilter(field_name='base_price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='base_price', lookup_expr='lte')

    class Meta:
        model = Flight
        fields = [
            'source_id', 'destination_id', 
            'source_city', 'destination_city', 
            'date', 'min_price', 'max_price'
        ]