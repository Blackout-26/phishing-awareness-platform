from django.db import models
from django.conf import settings
from simple_history.models import HistoricalRecords

class Campaign(models.Model):
    # Campaign Lifecycle States [cite: 54]
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('active', 'Active'),
        ('completed', 'Completed'),
    )

    name = models.CharField(max_length=255, help_text="The internal name of the phishing campaign.")
    
    # New Field: Description for administrative notes
    description = models.TextField(blank=True, null=True, help_text="Internal notes about the campaign objectives.") # 
    
    # The Architectural Anchor: Link to the Organization [cite: 52]
    organization = models.ForeignKey(
        'organizations.Organization', 
        on_delete=models.CASCADE, 
        related_name='campaigns',
        help_text="The organization this campaign belongs to."
    )

    # New Field: Linking to the Email Template [cite: 56]
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
    
    # Scheduling [cite: 30]
    start_date = models.DateTimeField(null=True, blank=True, help_text="When the campaign should start sending emails.")
    end_date = models.DateTimeField(null=True, blank=True, help_text="When the campaign stops tracking interactions.")
    
    # Audit timestamps and ownership
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE,
        help_text="The user who created this campaign."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Enterprise Audit Trail [cite: 60]
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.name} ({self.organization.name})"