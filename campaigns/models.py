from django.db import models
from simple_history.models import HistoricalRecords

class Campaign(models.Model):
    # Campaign Lifecycle States
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('completed', 'Completed'),
    )

    name = models.CharField(max_length=255, help_text="The internal name of the phishing campaign.")
    
    # The Architectural Anchor: Link to the Organization
    organization = models.ForeignKey(
        'organizations.Organization', 
        on_delete=models.CASCADE, 
        related_name='campaigns',
        help_text="The organization this campaign belongs to."
    )
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='draft',
        help_text="The current state of the campaign."
    )
    
    # Scheduling
    start_date = models.DateTimeField(null=True, blank=True, help_text="When the campaign should start sending emails.")
    end_date = models.DateTimeField(null=True, blank=True, help_text="When the campaign stops tracking interactions.")
    
    # Audit timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Enterprise Audit Trail
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.name} ({self.organization.name})"