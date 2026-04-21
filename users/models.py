from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
from .choices import UserRole

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is a required field')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('first_name', 'Admin')
        extra_fields.setdefault('last_name', 'Adminov')
        extra_fields.setdefault('role', UserRole.SYSTEM_ADMIN) 
        
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None  
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    
    role = models.CharField(
        max_length=20,
        choices=UserRole.choices,
        default=UserRole.CUSTOMER
    )
    
    managed_airport = models.ForeignKey(
        'airports.Airport', 
        on_delete=models.SET_NULL, 
        null=True, blank=True,
        related_name='managers',
        verbose_name=_("Managed Airport")
    )
    
    managed_airline = models.ForeignKey(
        'airports.Airline', 
        on_delete=models.SET_NULL, 
        null=True, blank=True,
        related_name='managers',
        verbose_name=_("Managed Airline")
    )
    
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    passport_number = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name'] 


    @property
    def is_system_admin(self):
        return self.is_superuser or self.is_staff or self.role == UserRole.SYSTEM_ADMIN

    @property
    def is_airport_manager(self):
        return self.role == UserRole.AIRPORT_ADMIN and self.managed_airport is not None

    @property
    def is_airline_manager(self):
        return self.role == UserRole.AIRLINE_ADMIN and self.managed_airline is not None

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"