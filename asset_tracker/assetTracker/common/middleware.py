# Custom Middleware file.
from django.http import HttpResponseForbidden
from assetTracker.settings import ALLOWED_REQUEST_HOSTS
from common.messages import get_message

class HostCheckMiddleware:
    """
    HostCheckMiddleware will verify the request host and will return 
    Exception or Response according to the ALLOWED REQUEST HOST specified 
    in project settings.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        self.allowed_request_hosts = ALLOWED_REQUEST_HOSTS

    def __call__(self, request):
        # Get the request's host
        request_host = request.get_host()

        # Check if the request's host is in the list of allowed hosts
        if request_host not in self.allowed_request_hosts:
            # Return a forbidden response if the host is not allowed
            return HttpResponseForbidden(get_message("INVALID_HOST"))
                
        # Allow the request to continue to the view for allowed hosts
        return self.get_response(request)

