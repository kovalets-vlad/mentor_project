from rest_framework import permissions
from .choices import UserRole

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj == request.user:
            return True
            
        if request.user.is_superuser or request.user.role == UserRole.SYSTEM_ADMIN:
            return True

        return False