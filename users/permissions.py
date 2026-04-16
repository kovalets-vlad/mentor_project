from rest_framework import permissions
from .choices import UserRole

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            if request.user.is_staff or request.user.role == UserRole.ADMIN:
                return True
            return obj == request.user 

        if obj == request.user:
            return True
            
        if request.user.is_superuser:
            return True

        if request.user.is_staff or request.user.role == UserRole.ADMIN:
            return obj.role == UserRole.CUSTOMER and not obj.is_superuser

        return False