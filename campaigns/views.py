from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone  # NEW: Import timezone for scheduling
from .forms import CampaignCreateForm
from .tasks import dispatch_campaign_emails  # Import our Celery task

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')

@login_required
def campaign_create_view(request):
    if request.method == 'POST':
        form = CampaignCreateForm(request.POST)
        if form.is_valid():
            # Save the campaign but don't commit to DB just yet
            campaign = form.save(commit=False)
            # Assign the user who created it
            campaign.created_by = request.user
            # Now save to the database so it gets an ID
            campaign.save()
            
            # 🚀 SCHEDULING LOGIC
            if campaign.start_date and campaign.start_date > timezone.now():
                # Schedule the task for the future using 'eta' (Estimated Time of Arrival)
                dispatch_campaign_emails.apply_async(args=[campaign.id], eta=campaign.start_date)
                
                # Format the time nicely for the UI notification
                formatted_time = campaign.start_date.strftime('%b %d, %Y at %I:%M %p')
                messages.success(request, f"Campaign '{campaign.name}' scheduled for deployment on {formatted_time}.")
            else:
                # No future date provided? Fire immediately using standard delay()
                dispatch_campaign_emails.delay(campaign.id)
                messages.success(request, f"Campaign '{campaign.name}' launched! Emails are being dispatched immediately.")
            
            return redirect('dashboard')
    else:
        form = CampaignCreateForm()
    
    return render(request, 'campaign_create.html', {'form': form})