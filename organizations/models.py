from django.db import models
from django.conf import settings
from simple_history.models import HistoricalRecords

class Organization(models.Model):
    name = models.CharField(max_length=255, unique=True, help_text="The official name of the organization.")
    # Link the organization to the user who created/manages it
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.RESTRICT, 
        related_name='owned_organizations',
        help_text="The primary administrator/owner of this organization account."
    )
    contact_email = models.EmailField(help_text="Primary contact email for security reports.")
    
    # Audit timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Enterprise Audit Trail
    history = HistoricalRecords()

    def __str__(self):
        return self.name