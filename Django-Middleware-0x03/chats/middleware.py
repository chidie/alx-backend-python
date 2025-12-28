from datetime import datetime

class RequestLoggingMiddleware:
    def __init__(self, get_response):
        # get_response is the next middleware or the view
        self.get_response = get_response

    
    def ___call___(self, request):
        # Determine the user (authenticated or Anonymous)
        user = request.user if getattr(request, "user", None) and request.user.is_authenticated else "Anonymous"
        log_line = f"{datetime.now()} - User: {user} - Path: {request.path}\n"

        with open("requests.log", "a") as log_file:
            log_file.write(log_line)

        response = self.get_response(request)
        return response
    
    