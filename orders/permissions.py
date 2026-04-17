from rest_framework import permissions
from users.choices import UserRole

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_staff or request.user.role == UserRole.ADMIN:
            return True

        if hasattr(obj, 'user'):
            return obj.user == request.user
            
        if hasattr(obj, 'order'):
            return obj.order.user == request.user

        return False