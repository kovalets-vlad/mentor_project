from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CountryViewSet, AirportViewSet, AirlineViewSet ,AirplaneTypeViewSet, AirplaneViewSet

router = DefaultRouter()
router.register(r'countries', CountryViewSet, basename="countries")
router.register(r'airports', AirportViewSet, basename="airports")
router.register(r'airlines', AirlineViewSet, basename="airlines")
router.register(r'airplane-types', AirplaneTypeViewSet, basename="airplane-types")
router.register(r'airplanes', AirplaneViewSet, basename="airplanes")


urlpatterns = [
    path('', include(router.urls)),
]