from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import get_user_model

from .serializers import (
    RegisterSerializer, 
    UserShortSerializer, 
    UserDetailSerializer, 
    UserAdminUpdateSerializer
)
from .permissions import IsOwnerOrAdmin
from core.permissions import IsSystemAdminOrReadOnly 

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    
    def get_serializer_class(self):
        if self.action == 'create':
            return RegisterSerializer
            
        if self.action == 'list':
            return UserShortSerializer

        if self.action in ['update', 'partial_update']:
            if self.request.user.is_system_admin:
                return UserAdminUpdateSerializer
            return UserDetailSerializer

        return UserDetailSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
            
        if self.action == 'list':
            return [IsSystemAdminOrReadOnly()] 
            
        if self.action in ['retrieve', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated(), IsOwnerOrAdmin()]
            
        return [IsAuthenticated()]