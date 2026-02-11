"""
Custom middleware for enhanced error handling and logging.
Implements production-ready middleware following Django best practices.
"""
import logging
import traceback
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.conf import settings

logger = logging.getLogger(__name__)


class ErrorHandlingMiddleware:
    """
    Middleware to catch and handle exceptions globally.
    Provides better error messages and logging for production environments.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as e:
            return self.handle_exception(request, e)
    
    def handle_exception(self, request, exception):
        """
        Handle exceptions that occur during request processing.
        
        Args:
            request: The HTTP request
            exception: The exception that was raised
            
        Returns:
            Appropriate error response based on request type
        """
        # Log the full exception with traceback
        logger.error(
            f"Unhandled exception in middleware: {str(exception)}\n"
            f"Path: {request.path}\n"
            f"Method: {request.method}\n"
            f"User: {request.user if hasattr(request, 'user') and request.user.is_authenticated else 'Anonymous'}\n"
            f"Traceback: {traceback.format_exc()}"
        )
        
        # Return JSON response for AJAX requests
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'error': 'An unexpected error occurred.',
                'message': str(exception) if settings.DEBUG else 'Please try again later.'
            }, status=500)
        
        # Return HTML error page for regular requests
        try:
            context = {
                'error_message': str(exception) if settings.DEBUG else 'Something went wrong. Please try again later.',
                'debug': settings.DEBUG,
                'traceback': traceback.format_exc() if settings.DEBUG else None,
            }
            return render(request, '500.html', context, status=500)
        except Exception as render_error:
            # Fallback if rendering template fails
            logger.error(f"Error rendering error page: {str(render_error)}")
            return HttpResponse(
                'A critical error occurred. Please contact support.',
                status=500
            )
    
    def process_exception(self, request, exception):
        """
        Django's built-in exception processor hook.
        Called when a view raises an exception.
        """
        if settings.DEBUG:
            return None
        return self.handle_exception(request, exception)


class SecurityHeadersMiddleware:
    """
    Middleware to add security headers to all responses.
    Implements OWASP security best practices.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        
        # Add security headers
        if not settings.DEBUG:
            response['X-Content-Type-Options'] = 'nosniff'
            response['X-Frame-Options'] = 'DENY'
            response['X-XSS-Protection'] = '1; mode=block'
            response['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        
        return response
