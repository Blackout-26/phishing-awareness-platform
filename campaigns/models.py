from django.db import models
from django.conf import settings
from simple_history.models import HistoricalRecords

class Campaign(models.Model):
    # Campaign Lifecycle States
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('completed', 'Completed'),
    )

    name = models.CharField(max_length=255, help_text="The internal name of the phishing campaign.")
    
    # Description for administrative notes
    description = models.TextField(blank=True, null=True, help_text="Internal notes about the campaign objectives.")
    
    # The Architectural Anchor: Link to the Organization
    organization = models.ForeignKey(
        'organizations.Organization', 
        on_delete=models.CASCADE, 
        related_name='campaigns',
        help_text="The organization this campaign belongs to."
    )

    # Linking to the Email Template
    template = models.ForeignKey(
        'email_templates.EmailTemplate',
        on_delete=models.CASCADE,
        related_name='campaigns',
        help_text="The phishing template to be used for this campaign."
    )
    
    status = models.CharField(
        max_length=20, 
        choices=STATUS_CHOICES, 
        default='draft',
        help_text="The current state of the campaign."
    )
    
    # 🚀 Scheduling Fields
    start_date = models.DateTimeField(
        null=True, 
        blank=True, 
        help_text="When the campaign should start sending emails. Leave blank for immediate dispatch."
    )
    end_date = models.DateTimeField(
        null=True, 
        blank=True, 
        help_text="When the campaign stops tracking interactions."
    )
    
    # Audit timestamps and ownership
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        help_text="The user who created this campaign."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Enterprise Audit Trail
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.name} ({self.organization.name})"