import os
import logging
from datetime import datetime

class RequestLoggingMiddleware:
    """
    Middleware to log the start and end time of each request.
    """

    def __init__(self, get_response):
        self.get_response = get_response
        log_dir = os.path.dirname(__file__)
        requested_log_path = os.path.join(log_dir, 'requests.log')
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