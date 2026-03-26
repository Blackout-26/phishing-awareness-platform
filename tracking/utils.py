import secrets
import string

def generate_tracking_token(length=32):
    """
    Generates a cryptographically secure, random URL-safe token.
    Combines ascii letters and digits to avoid predictable patterns.
    """
    alphabet = string.ascii_letters + string.digits
    return ''.join(secrets.choice(alphabet) for _ in range(length))