from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CountryViewSet, AirportViewSet, AirlineViewSet ,AirplaneTypeViewSet, AirplaneViewSet

router = DefaultRouter()
router.register(r'countries', CountryViewSet)
router.register(r'airports', AirportViewSet)
router.register(r'airlines', AirlineViewSet)
router.register(r'airplane-types', AirplaneTypeViewSet)
router.register(r'airplanes', AirplaneViewSet)


urlpatterns = [
    path('', include(router.urls)),
]