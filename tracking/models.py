from django.db import models
from simple_history.models import HistoricalRecords
from .utils import generate_tracking_token
from django.conf import settings

class TrackingLink(models.Model):
    """
    Generates and stores the secure, unique token for each TargetUser in a Campaign.
    This acts as the unique bridge between an email and the telemetry events.
    """
    campaign = models.ForeignKey('campaigns.Campaign', on_delete=models.CASCADE, related_name='tracking_links')
    target = models.ForeignKey('targets.TargetUser', on_delete=models.CASCADE, related_name='tracking_links')
    
    # The secure token field
    token = models.CharField(
        max_length=64, 
        unique=True, 
        default=generate_tracking_token, 
        db_index=True, # Indexed for extremely fast database lookups when a click happens
        help_text="Cryptographically secure token for URL tracking."
    )
    
    # Quick-reference state
    is_clicked = models.BooleanField(default=False)
    clicked_at = models.DateTimeField(null=True, blank=True)
    
    # Audit timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"Token for {self.target.email} - {self.campaign.name}"

    @property
    def get_tracking_url(self):
        """Generates the full tracking URL for the target to click"""
        # Falls back to localhost for development if BASE_URL isn't in settings
        base_url = getattr(settings, 'BASE_URL', 'http://127.0.0.1:8000')
        return f"{base_url}/track/{self.token}/"


class ClickEvent(models.Model):
    campaign = models.ForeignKey('campaigns.Campaign', on_delete=models.CASCADE, related_name='click_events')
    target = models.ForeignKey('targets.TargetUser', on_delete=models.CASCADE, related_name='click_events')
    
    # Telemetry data
    ip_address = models.GenericIPAddressField(null=True, blank=True, help_text="Used to filter out automated security scanners.")
    user_agent = models.TextField(blank=True)
    
    # Audit timestamps
    timestamp = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"Click: {self.target.email} at {self.timestamp}"


class SubmissionEvent(models.Model):
    campaign = models.ForeignKey('campaigns.Campaign', on_delete=models.CASCADE, related_name='submission_events')
    target = models.ForeignKey('targets.TargetUser', on_delete=models.CASCADE, related_name='submission_events')
    
    # Telemetry data
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    
    # We only log the boolean event, never the actual sensitive payload
    is_compromised = models.BooleanField(default=True, help_text="Did the target submit data to the simulated landing page?")
    
    # Audit timestamps
    timestamp = models.DateTimeField(auto_now_add=True)
    history = HistoricalRecords()

    def __str__(self):
        return f"Submission: {self.target.email} at {self.timestamp}"