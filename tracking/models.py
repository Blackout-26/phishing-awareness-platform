from django.db import models
from simple_history.models import HistoricalRecords

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