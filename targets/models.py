from django.db import models
from simple_history.models import HistoricalRecords

class TargetUser(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )

    email = models.EmailField(help_text="The email address of the target recipient.")
    first_name = models.CharField(max_length=150, blank=True, help_text="Target's first name (for email template injection).")
    last_name = models.CharField(max_length=150, blank=True, help_text="Target's last name.")
    department = models.CharField(max_length=100, blank=True, help_text="Department for risk segmentation (e.g., HR, Finance).")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', help_text="Inactive targets will be excluded from campaigns.")
    
    # Tie the target to a specific organization for multi-tenant isolation
    organization = models.ForeignKey(
        'organizations.Organization', 
        on_delete=models.CASCADE, 
        related_name='target_users',
        help_text="The organization this target belongs to."
    )
    
    # Audit timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Enterprise Audit Trail
    history = HistoricalRecords()

    class Meta:
        # A user can only be added once per organization, but the same email could exist in different orgs (e.g. an external consultant)
        unique_together = ('organization', 'email')

    def __str__(self):
        return f"{self.email} ({self.organization.name})"