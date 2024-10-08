# accounts/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('client', 'Client'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='client')
    username = models.CharField(max_length=20, unique=True, null=False, blank=False)  # Ensure username is unique and required
    email = models.EmailField(max_length=30, unique=True, null=False, blank=False)  # Email field, unique and required
    password = models.CharField(max_length=128, null=False, blank=False)  # Password field, required

    def __str__(self):
        return self.username


# models.py

import uuid
class EmailVerificationCode(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
