from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.is_system_admin:
            return True

        if hasattr(obj, 'user'):
            return obj.user == request.user
            
        if hasattr(obj, 'order'):
            return obj.order.user == request.user

        return False