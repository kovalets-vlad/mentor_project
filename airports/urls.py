from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CountryListCreateView, CountryDetailView, AirportViewSet, AirlineViewSet ,AirplaneTypeViewSet, AirplaneViewSet

router = DefaultRouter()
router.register(r'airports', AirportViewSet, basename="airports")
router.register(r'airlines', AirlineViewSet, basename="airlines")
router.register(r'airplane-types', AirplaneTypeViewSet, basename="airplane-types")
router.register(r'airplanes', AirplaneViewSet, basename="airplanes")


urlpatterns = [
    path('', include(router.urls)),
    path('countries/', CountryListCreateView.as_view(), name='country-list'),
    path('countries/<int:pk>/', CountryDetailView.as_view(), name='country-detail'),
]