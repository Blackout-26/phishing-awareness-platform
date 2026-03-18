from django.db import models
from simple_history.models import HistoricalRecords

class EmailTemplate(models.Model):
    name = models.CharField(max_length=255, help_text="Internal name for this template (e.g., 'IT Password Reset').")
    
    # Tie the template to a specific organization for multi-tenant isolation
    organization = models.ForeignKey(
        'organizations.Organization', 
        on_delete=models.CASCADE, 
        related_name='email_templates',
        help_text="The organization that owns this template."
    )
    
    # The actual email content
    subject = models.CharField(max_length=255, help_text="The email subject line. Supports variables like {{ target_name }}.")
    text_body = models.TextField(help_text="The plain-text version of the email. Supports variables.")
    html_body = models.TextField(help_text="The HTML version of the email. Supports variables and tracking links.")
    
    # Audit timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Enterprise Audit Trail
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.name} ({self.organization.name})"