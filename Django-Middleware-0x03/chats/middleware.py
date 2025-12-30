import os
import logging
from datetime import datetime, time, timedelta
from django.conf import settings
from django.http import HttpResponseForbidden

class RequestLoggingMiddleware:
    """
    Middleware to log the start and end time of each request.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        log_dir = os.path.dirname(__file__)
        requested_log_path = os.path.abspath(os.path.join(log_dir, "..", "requests.log"))

        logging.basicConfig(
            filename=requested_log_path,
            level=logging.INFO,
            format='%(message)s'
        )

    def __call__(self, request):
        user = request.user if request.user.is_authenticated else 'Anonymous'
        log_entry = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logging.info(log_entry)

        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    """
    Middleware to restrict access to certain views based on time of day.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        # self.restricted_start = time(22, 0)  # 10 PM
        # self.restricted_end = time(6, 0)     # 6 AM

    def __call__(self, request):
        # Define restricted hours: outside 6AM–9PM
        start_allowed = time(6, 0)
        end_allowed = time(21, 0)
        current_time = datetime.now().time()

        # If current_time is outside allowed range, block access
        if not (start_allowed <= current_time <= end_allowed):
            return HttpResponseForbidden("Access to this resource is restricted during this time.")
        
        response = self.get_response(request)
        return response

class OffensiveLanguageMiddleware:
    """
    Middleware to filter offensive language in messages.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.ip_request_log = {} # Store request timestamps per IP
        self.REQUEST_LIMIT = 5  # Max requests
        self.TIME_WINDOW = timedelta(minutes=1)  # Time window

    def __call__(self, request):
        # Only rate-limit POST requests (messages)
        if request.method == "POST":
            ip = self.get_client_ip(request)
            now = datetime.now()

            # Initialize list for this IP
            if ip not in self.ip_request_log:
                self.ip_request_log[ip] = []
            
            # Remove timestamps older than 1 minute
            self.ip_request_log[ip] = [
                ts for ts in self.ip_request_log[ip] if now - ts < self.TIME_WINDOW
            ]

            self.ip_request_log[ip].append(now)
        
        return self.get_response(request)

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            return x_forwarded_for.split(',')[0]
        return request.META.get('REMOTE_ADDR')