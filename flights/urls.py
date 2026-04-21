from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RouteViewSet, FlightViewSet

router = DefaultRouter()
router.register(r'routes', RouteViewSet, basename='routes')
router.register(r'flights', FlightViewSet, basename='flight')


urlpatterns = [
    path('', include(router.urls)),
]
