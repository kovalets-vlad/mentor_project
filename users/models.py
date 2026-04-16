from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
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
        extra_fields.setdefault('role', UserRole.ADMIN) 
        
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
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    passport_number = models.CharField(max_length=20, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name'] 

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.email})"