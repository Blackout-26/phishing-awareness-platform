from celery import shared_task
from django.core.mail import send_mail
from django.conf import settings
from campaigns.models import Campaign
from tracking.models import TrackingLink

@shared_task
def dispatch_campaign_emails(campaign_id):
    """
    Background worker task to generate unique tracking tokens,
    inject them into the email template, and dispatch via Resend SMTP.
    """
    try:
        # 1. Fetch the campaign and its associated email template
        campaign = Campaign.objects.get(id=campaign_id)
        
        # 🚀 NEW: Flip the status to active now that the dispatch has begun!
        campaign.status = 'active'
        campaign.save()
        
        template = campaign.template
        
        # 2. Get all targets assigned to this campaign's organization
        targets = campaign.organization.target_users.all() 
        
        success_count = 0

        # 3. Loop through each target, generate a token, and send the email
        for target in targets:
            # Create a unique tracking token for this specific target
            tracking_record = TrackingLink.objects.create(
                campaign=campaign,
                target=target
            )
            
            # Use the helper property we added to get the full localhost or production URL
            tracking_url = tracking_record.get_tracking_url
            
            # Inject the tracking link and target's info into the email body
            customized_body = template.body.replace('{{ tracking_link }}', tracking_url)
            
            # Only replace first_name if you used it in your template and it exists on TargetUser
            if hasattr(target, 'first_name') and target.first_name:
                customized_body = customized_body.replace('{{ first_name }}', target.first_name)

            # Fire the email via the configured SMTP backend (Resend)
            send_mail(
                subject=template.subject,
                message=customized_body, # Plain text fallback
                from_email=f"{template.sender_name} <{settings.DEFAULT_FROM_EMAIL}>",
                recipient_list=[target.email],
                html_message=customized_body, # HTML version
                fail_silently=False,
            )
            success_count += 1
            
        # Note: We leave the status as 'active' rather than 'completed'.
        # The emails are sent, but the campaign is still "active" because we are tracking clicks!
        
        return f"SUCCESS: Dispatched {success_count} emails for campaign '{campaign.name}'"

    except Exception as e:
        return f"FAILED: {str(e)}"