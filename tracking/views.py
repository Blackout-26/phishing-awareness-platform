from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponse
from .models import TrackingLink, ClickEvent, SubmissionEvent

def get_client_ip(request):
    """Helper function to cleanly extract the real IP address from the request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def detect_bot(user_agent):
    """
    Checks the User-Agent string against a list of known email security scanners and web crawlers.
    """
    if not user_agent:
        return False
        
    bot_signatures = [
        'bot', 'crawler', 'spider', 'slurp', 'google-read-aloud', 
        'googleimageproxy', 'microsoftpreview', 'mimecast', 'barracuda',
        'proofpoint', 'yandex', 'bingbot'
    ]
    user_agent_lower = user_agent.lower()
    return any(sig in user_agent_lower for sig in bot_signatures)

def track_click_view(request, token):
    """
    Validates the token, logs the click event (filtering bots), and redirects to the simulation page.
    """
    # 1. Resolve the secure token. If it doesn't exist, return a 404.
    tracking_link = get_object_or_404(TrackingLink, token=token)

    # 2. Extract basic telemetry data
    ip_address = get_client_ip(request)
    user_agent = request.META.get('HTTP_USER_AGENT', '')[:255] # Truncated for database safety
    
    # 3. Evaluate if this request is from an automated scanner
    is_scanner_bot = detect_bot(user_agent)

    # 4. Securely record the immutable ClickEvent, flagging it if it's a bot
    ClickEvent.objects.create(
        campaign=tracking_link.campaign,
        target=tracking_link.target,
        ip_address=ip_address,
        user_agent=user_agent,
        is_bot=is_scanner_bot
    )

    # 5. Update the TrackingLink quick-reference state ONLY if it was a real human interaction
    if not is_scanner_bot and not tracking_link.is_clicked:
        tracking_link.is_clicked = True
        tracking_link.clicked_at = timezone.now()
        tracking_link.save()

    # 6. Redirect to the phishing simulation landing page
    # Notice we use 'tracking:simulation_landing' to respect the app namespace
    return redirect('tracking:simulation_landing', token=token)

def simulation_landing(request, token):
    """
    The fake login page. 
    GET: Renders the fake login form.
    POST: Logs the submission event (credential compromise) and redirects to education.
    """
    tracking_link = get_object_or_404(TrackingLink, token=token)
    
    if request.method == "POST":
        # The target fell for the simulation and submitted the form!
        # Securely log the interaction. Notice we DO NOT extract or save the password.
        SubmissionEvent.objects.create(
            campaign=tracking_link.campaign,
            target=tracking_link.target,
            ip_address=get_client_ip(request),
            user_agent=request.META.get('HTTP_USER_AGENT', '')[:255],
            is_compromised=True
        )
        
        # Instantly redirect them to the educational training page
        return redirect('tracking:education_page', token=token)
        
    # If it's a GET request, render the fake login HTML template
    context = {
        'target': tracking_link.target,
        'token': token,
    }
    return render(request, 'tracking/fake_login.html', context)

def education_page(request, token):
    """
    The friendly 'Oops, this was a security simulation' page.
    """
    tracking_link = get_object_or_404(TrackingLink, token=token)
    
    context = {
        'target': tracking_link.target,
        'campaign': tracking_link.campaign
    }
    return render(request, 'tracking/education.html', context)