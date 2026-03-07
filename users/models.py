from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    ROLE = [
        ('admin', 'Admin'),
        ('operator', 'Operator'),
        ('boss', 'Boss'),
    ]
    
    username = models.CharField(max_length=150, unique=True)
    role = models.CharField(max_length=50, choices=ROLE, default='operator')
    
    
