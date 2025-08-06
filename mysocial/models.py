from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if email is None:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)  
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields.get('is_staff'):
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields.get('is_superuser'):
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)



class User(AbstractUser):
    username = None  # ✅ Remove username field from AbstractUser
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    mobile_no = models.CharField(max_length=11)
    email = models.EmailField(unique=True)
    photo = models.ImageField(upload_to='photos/', default='photos/default.png')

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] 

    objects = UserManager()

    def __str__(self):
        return self.email 



class OTP(models.Model):
    email = models.EmailField(max_length=255)
    otp = models.CharField(max_length=6)

    def __str__(self):
        return f'{self.email} ---- {self.otp}'