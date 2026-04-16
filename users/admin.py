from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    ordering = ('email',)
    
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff_member')
    
    search_fields = ('email', 'first_name', 'last_name')

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Персональна інформація', {'fields': ('first_name', 'last_name')}),
        ('Авіа-дані', {'fields': ('role', 'phone_number', 'passport_number', 'date_of_birth')}),
        ('Права доступу', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Важливі дати', {'fields': ('last_login', 'date_joined')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password', 'first_name', 'last_name', 'role'),
        }),
    )