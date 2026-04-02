from django.shortcuts import get_object_or_404, redirect
from django.utils import timezone
from django.http import HttpResponse
from .models import TrackingLink, ClickEvent

def get_client_ip(request):
    """Helper function to cleanly extract the real IP address from the request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def track_click_view(request, token):
    """
    Validates the token, logs the click event, and redirects to the simulation page.
    """
    # 1. Resolve the secure token. If it doesn't exist, return a 404.
    tracking_link = get_object_or_404(TrackingLink, token=token)

    # 2. Extract basic telemetry data
    ip_address = get_client_ip(request)
    user_agent = request.META.get('HTTP_USER_AGENT', '')[:255] # Truncated for database safety

    # 3. Securely record the immutable ClickEvent
    ClickEvent.objects.create(
        campaign=tracking_link.campaign,
        target=tracking_link.target,
        ip_address=ip_address,
        user_agent=user_agent
    )

    # 4. Update the TrackingLink quick-reference state if it's the first time being clicked
    if not tracking_link.is_clicked:
        tracking_link.is_clicked = True
        tracking_link.clicked_at = timezone.now()
        tracking_link.save()

    # 5. Redirect to the phishing simulation landing page
    return redirect('simulation_landing', token=token)

def simulation_landing_placeholder(request, token):
    """
    A temporary placeholder for the landing page until we build the real one.
    """
    return HttpResponse(f"<h1>Simulated Login Page</h1><p>Target Successfully Tracked. Your token is: {token}</p>")