from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    # Define the roles based on the engineering plan
    ROLE_CHOICES = (
        ('admin', 'Administrator'),
        ('analyst', 'Security Analyst'),
    )
    
    role = models.CharField(
        max_length=20, 
        choices=ROLE_CHOICES, 
        default='analyst',
        help_text="Designates the user's access level."
    )

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"