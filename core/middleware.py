from django.shortcuts import redirect
from django.urls import reverse

class UserAdminRestrictionMiddleware:
    """
    Middleware to restrict User Administrators to only the role management
    dashboard. They are explicitly forbidden from using other app features 
    or maintaining a basic user profile within the application.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and getattr(request.user, 'is_user_admin', False):
            # Paths that User Administrators are allowed to access
            allowed_prefixes = [
                reverse('role_management'),
                '/accounts/',  # logout, etc.
                '/admin/',     # builtin django admin, just in case they are staff/superuser
                '/static/',    # static files
            ]
            
            # Allow access if the path starts with any of the allowed prefixes
            if not any(request.path.startswith(prefix) for prefix in allowed_prefixes):
                return redirect('role_management')

        return self.get_response(request)
