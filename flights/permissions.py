from rest_framework import permissions

class IsAirportManagerOrSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        user = request.user
        return user.is_authenticated and (user.is_system_admin or user.is_airport_manager)

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        user = request.user
        if user.is_system_admin:
            return True

        source_airport = getattr(obj, 'source', None) or getattr(obj.route, 'source', None)
        
        return user.is_airport_manager and source_airport == user.managed_airport


class IsFlightManagerOrSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        
        user = request.user
        return user.is_authenticated and (
            user.is_system_admin or 
            user.is_airport_manager or 
            user.is_airline_manager
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
            
        user = request.user
        if user.is_system_admin:
            return True
            
        if user.is_airline_manager:
            return obj.airplane.airline == user.managed_airline
            
        if user.is_airport_manager:
            return obj.route.source == user.managed_airport
            
        return False