from django.contrib.auth.models import AbstractUser
from django.db import models
from simple_history.models import HistoricalRecords

class CustomUser(AbstractUser):
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
    
    # This single line tracks every change made to this model
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"