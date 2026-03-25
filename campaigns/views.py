from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import CampaignCreateForm

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')

@login_required
def campaign_create_view(request):
    if request.method == 'POST':
        form = CampaignCreateForm(request.POST)
        if form.is_valid():
            campaign = form.save(commit=False)
            campaign.created_by = request.user
            campaign.save()
            return redirect('dashboard')
    else:
        form = CampaignCreateForm()
    
    return render(request, 'campaign_create.html', {'form': form})