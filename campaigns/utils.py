import requests
import logging

logger = logging.getLogger(__name__)

def get_ip_location(ip_address):
    """
    Uses the free ip-api.com service to resolve an IP address to a physical location.
    """
    # Filter out localhost IPs for local testing
    if ip_address in ['127.0.0.1', 'localhost', None, '']:
        return "Local Network / Unknown"

    try:
        # We only request the fields we need to save bandwidth
        response = requests.get(f"http://ip-api.com/json/{ip_address}?fields=status,country,city")
        data = response.json()
        
        if data.get('status') == 'success':
            return f"{data.get('city', 'Unknown City')}, {data.get('country', 'Unknown Country')}"
        return "Unknown Location"
    except Exception as e:
        logger.error(f"Geolocation failed for IP {ip_address}: {e}")
        return "Location Lookup Failed"