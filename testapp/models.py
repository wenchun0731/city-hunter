from django.db import models
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from decimal import Decimal
from django.utils import timezone

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)  
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
    uploaded_at = models.DateTimeField(auto_now_add=True)  

    def __str__(self):
        return self.video_file.name
    
class Car(models.Model):
    id = models.AutoField(primary_key=True)
    license_plate = models.CharField(max_length=100)  
    date_time = models.DateTimeField()  
    location = models.CharField(max_length=255)  
    violation = models.CharField(max_length=16, blank=True, null=True, default='')  
    seconds = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal('0.00'))
    car_image = models.ImageField(upload_to='car_images/', blank=True, null=True, verbose_name="車輛圖片")
    plate_image = models.ImageField(upload_to='plate_images/', blank=True, null=True, verbose_name="車牌圖片")  # New field

    def save(self, *args, **kwargs):
        # 將地點轉換為大寫再儲存
        if self.location:
            self.location = self.location.upper()
        super().save(*args, **kwargs)

    def __str__(self):
        violation_status = self.violation if self.violation else '未違規'
        return f"車輛ID: {self.id}, 車牌: {self.license_plate}, 日期時間: {self.date_time}, 地點: {self.location}, 違規狀態: {violation_status}"



class Vehicle(models.Model):
    license_plate = models.CharField(max_length=10, verbose_name="車牌")
    date_time = models.DateTimeField(verbose_name="日期時間")
    location = models.CharField(max_length=255, verbose_name="地點")
    violation = models.CharField(max_length=50, verbose_name="違規種類")
    image_url = models.URLField(verbose_name="違規影片")

    def __str__(self):
        return f'{self.license_plate} - {self.date_time}'

    class Meta:
        verbose_name = '車輛'
        verbose_name_plural = '車辆'
        
class Record(models.Model):
    license_plate = models.CharField(max_length=20)
    date_time = models.DateTimeField()
    location = models.CharField(max_length=100)
    violation = models.CharField(max_length=50)
    image_url = models.URLField()

    def __str__(self):
        return self.license_plate
