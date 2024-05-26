from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)  # Hash the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
        
    def last_login(self):
        return None

    def set_last_login(self, value):
        pass

    def get_last_login(self):
        return None

    
class Video(models.Model):
    video_file = models.FileField(upload_to='videos/') 
    
class Car(models.Model):
    id = models.AutoField(primary_key=True)
    license_plate = models.CharField(max_length=100)  
    date_time = models.DateTimeField()  
    location = models.CharField(max_length=255)  
    VIOLATION_CHOICES = [
        (False, 'No'),
        (True, 'Yes'),
    ]
    violation = models.BooleanField(choices=VIOLATION_CHOICES, default=False)

    def __str__(self):
        return f"Car ID: {self.id}, License Plate: {self.license_plate}, Date Time: {self.date_time}, Location: {self.location}, Violation: {self.get_violation_display()}"










