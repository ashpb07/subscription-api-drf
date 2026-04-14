from django.utils.deprecation import MiddlewareMixin
from django.contrib.auth.models import AnonymousUser
from users.models import UserProfile
from analytics.models import Log,Traffic
from common.utils import get_client_ip


class RequestLogMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if hasattr(request, "user") and request.user.is_authenticated:
            Log.objects.create(
                user=request.user,
                action=request.path,
                status=response.status_code
            )

        return response
    





class TrafficAnalyticsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        
        if request.path.startswith('/api/'):
            Traffic.objects.create(
               
                user=request.user if request.user.is_authenticated else None,
                status=response.status_code,
                ip_address=get_client_ip(request),
                path=request.path,
                method=request.method,
            )
        return response
