from django.core.exceptions import PermissionDenied
from functools import wraps

def role_required(allowed_roles):
    """
    Master decorator to check if a user has a specific role.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.role in allowed_roles:
                return view_func(request, *args, **kwargs)
            # Boot them out if they don't have the right role
            raise PermissionDenied 
        return _wrapped_view
    return decorator

# Specific decorators you can easily import into your views later
def admin_required(view_func):
    return role_required(['admin'])(view_func)

def analyst_required(view_func):
    return role_required(['admin', 'analyst'])(view_func)