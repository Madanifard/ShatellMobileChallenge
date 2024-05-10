from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from .managers import CustomUserManager
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password, check_password



class AdminUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    password = models.TextField()
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def validate_password(self, raw_password):
        return check_password(raw_password, self.password)
    

#TODO: CREATE ADMIN PANEL FOR THIS, and create TEST
class UserInfo(models.Model):
    email = models.EmailField(unique=True)
    national_id = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f'{self.email} - {self.national_id}'