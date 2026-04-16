from rest_framework import permissions
from users.choices import UserRole

class IsAdminOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
            
        return bool(
            request.user and 
            request.user.is_authenticated and 
            (request.user.is_staff or request.user.role == UserRole.ADMIN)
        )