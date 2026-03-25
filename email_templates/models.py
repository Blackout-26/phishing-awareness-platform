from django.db import models
from simple_history.models import HistoricalRecords

class EmailTemplate(models.Model):
    name = models.CharField(max_length=255, help_text="Internal name of the template.")
    subject = models.CharField(max_length=255, help_text="The subject line of the phishing email.")
    
    # The fields the form was looking for:
    body = models.TextField(help_text="The HTML or plain text body of the email.")
    sender_name = models.CharField(max_length=255, help_text="The name the email appears to be from (e.g., IT Support).")
    sender_email = models.EmailField(help_text="The email address the email appears to be from.")
    
    organization = models.ForeignKey(
        'organizations.Organization', 
        on_delete=models.CASCADE, 
        related_name='email_templates'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Enterprise Audit Trail
    history = HistoricalRecords()

    def __str__(self):
        return f"{self.name} ({self.organization.name})"