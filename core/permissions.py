from rest_framework import permissions

class IsSystemAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
            
        return bool(
            request.user and 
            request.user.is_authenticated and 
            request.user.is_system_admin 
        )
    
class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser or request.user.is_system_admin:
            return True
        
        if hasattr(obj, 'airline'):
            return obj.airline == request.user.managed_airline
        
        if hasattr(obj, 'source'):
            return obj.source == request.user.managed_airport
            
        return False

class IsAirlineManagerOrSuperAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
            
        user = request.user
        
        return bool(
            user and 
            user.is_authenticated and 
            (user.is_system_admin or user.is_airline_manager)
        )

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        user = request.user
        
        if user.is_system_admin:
            return True
            
        if user.is_airline_manager:
            return getattr(obj, 'airline', None) == user.managed_airline
            
        return False