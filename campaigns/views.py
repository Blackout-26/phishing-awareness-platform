import json
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone  
from django.db.models import Count, F
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa

from .forms import CampaignCreateForm
from .models import Campaign
from .tasks import dispatch_campaign_emails  
from tracking.models import TrackingLink, ClickEvent, SubmissionEvent
from .utils import get_ip_location # Import our new tool

@login_required
def dashboard_view(request):
    # Fetch all campaigns created by the user, newest first
    campaigns = Campaign.objects.filter(created_by=request.user).order_by('-created_at')
    
    # Pass the campaigns to the dashboard template
    return render(request, 'dashboard.html', {'campaigns': campaigns})

@login_required
def campaign_create_view(request):
    if request.method == 'POST':
        form = CampaignCreateForm(request.POST)
        if form.is_valid():
            campaign = form.save(commit=False)
            campaign.created_by = request.user
            campaign.save()
            
            # 🚀 SCHEDULING LOGIC
            if campaign.start_date and campaign.start_date > timezone.now():
                dispatch_campaign_emails.apply_async(args=[campaign.id], eta=campaign.start_date)
                formatted_time = campaign.start_date.strftime('%b %d, %Y at %I:%M %p')
                messages.success(request, f"Campaign '{campaign.name}' scheduled for deployment on {formatted_time}.")
            else:
                dispatch_campaign_emails.delay(campaign.id)
                messages.success(request, f"Campaign '{campaign.name}' launched! Emails are being dispatched immediately.")
            
            return redirect('dashboard')
    else:
        form = CampaignCreateForm()
    
    return render(request, 'campaign_create.html', {'form': form})

@login_required
def campaign_dashboard(request, pk):
    """
    Calculates and visualizes the human risk metrics for a specific campaign.
    """
    campaign = get_object_or_404(Campaign, pk=pk)

    # 1. Base Metrics
    total_targets = TrackingLink.objects.filter(campaign=campaign).count()

    human_clicks = ClickEvent.objects.filter(
        campaign=campaign,
        is_bot=False
    ).values('target').distinct().count()

    compromised = SubmissionEvent.objects.filter(
        campaign=campaign
    ).values('target').distinct().count()

    # 2. Calculate Rates & Scoring
    click_rate = round((human_clicks / total_targets * 100) if total_targets > 0 else 0, 1)
    submission_rate = round((compromised / total_targets * 100) if total_targets > 0 else 0, 1)
    
    # Awareness Score: A simple baseline metric (100% minus the compromise rate)
    awareness_score = 100 - submission_rate 

    # 3. Department Analytics
    department_stats = SubmissionEvent.objects.filter(
        campaign=campaign
    ).values(
        dept_name=F('target__department')
    ).annotate(
        compromised_count=Count('target', distinct=True)
    ).order_by('-compromised_count')

    # Prepare data arrays for Chart.js
    dept_labels = [stat['dept_name'] or 'Unknown' for stat in department_stats]
    dept_data = [stat['compromised_count'] for stat in department_stats]

    context = {
        'campaign': campaign,
        'total_targets': total_targets,
        'human_clicks': human_clicks,
        'compromised': compromised,
        'click_rate': click_rate,
        'submission_rate': submission_rate,
        'awareness_score': awareness_score,
        'dept_labels_json': json.dumps(dept_labels),
        'dept_data_json': json.dumps(dept_data),
    }

    return render(request, 'campaigns/dashboard.html', context)

@login_required
def campaign_pdf_report(request, pk):
    """
    Generates an automated executive PDF report for a specific campaign,
    including IP geolocation for compromised targets.
    """
    campaign = get_object_or_404(Campaign, pk=pk)

    # 1. Base Metrics (Same as Dashboard)
    total_targets = TrackingLink.objects.filter(campaign=campaign).count()
    human_clicks = ClickEvent.objects.filter(campaign=campaign, is_bot=False).values('target').distinct().count()
    compromised_events = SubmissionEvent.objects.filter(campaign=campaign).select_related('target')
    compromised_count = compromised_events.values('target').distinct().count()

    click_rate = round((human_clicks / total_targets * 100) if total_targets > 0 else 0, 1)
    submission_rate = round((compromised_count / total_targets * 100) if total_targets > 0 else 0, 1)
    awareness_score = 100 - submission_rate

    # 2. Geolocation Processing
    # We will grab the latest submission event for each compromised target to see where they were "hacked"
    compromised_details = []
    for event in compromised_events:
        location = get_ip_location(event.ip_address)
        compromised_details.append({
            'email': event.target.email,
            'department': event.target.department or 'Unknown',
            'ip': event.ip_address,
            'location': location,
            'timestamp': event.timestamp
        })

    # 3. Department Analytics
    department_stats = SubmissionEvent.objects.filter(campaign=campaign).values(
        dept_name=F('target__department')
    ).annotate(
        compromised_count=Count('target', distinct=True)
    ).order_by('-compromised_count')

    context = {
        'campaign': campaign,
        'total_targets': total_targets,
        'human_clicks': human_clicks,
        'compromised_count': compromised_count,
        'click_rate': click_rate,
        'submission_rate': submission_rate,
        'awareness_score': awareness_score,
        'department_stats': department_stats,
        'compromised_details': compromised_details,
        'generated_by': request.user.email,
        'date_generated': timezone.now()
    }

    # 4. PDF Generation Magic
    template = get_template('campaigns/pdf_report.html')
    html = template.render(context)
    
    # Create an HTTP response with the correct PDF headers
    response = HttpResponse(content_type='application/pdf')
    # Use 'attachment' to force download, or 'inline' to open in browser
    response['Content-Disposition'] = f'attachment; filename="Security_Report_{campaign.name}.pdf"'

    # Convert HTML to PDF using xhtml2pdf
    pisa_status = pisa.CreatePDF(html, dest=response)
    
    if pisa_status.err:
        return HttpResponse('We had some errors generating your report.', status=500)
    return response