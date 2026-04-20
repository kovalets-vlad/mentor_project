from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    ordering = ('email',)
    
    list_display = ('email', 'first_name', 'last_name', 'role', 'managed_airport', 'managed_airline', 'is_staff')
    
    search_fields = ('email', 'first_name', 'last_name')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Full name', {'fields': ('first_name', 'last_name')}),
        ('Personal information', {'fields': (
            'role', 'managed_airport', 'managed_airline', 
            'phone_number', 'passport_number', 'date_of_birth'
        )}),
        ('Access rights', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Date', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'first_name', 'last_name', 'role', 'managed_airport', 'managed_airline'),
        }),
    )