"""
Custom error handlers for production-ready error pages.
Provides user-friendly error pages with proper logging.
"""
import logging
from django.shortcuts import render
from django.http import HttpResponseNotFound, HttpResponseServerError

logger = logging.getLogger(__name__)


def handler404(request, exception=None):
    """
    Custom 404 error handler.
    
    Args:
        request: HTTP request that resulted in 404
        exception: Optional exception that caused the 404
        
    Returns:
        HttpResponseNotFound with custom template
    """
    logger.warning(
        f"404 Error: {request.path} - "
        f"Referrer: {request.META.get('HTTP_REFERER', 'None')} - "
        f"User: {request.user if request.user.is_authenticated else 'Anonymous'}"
    )
    
    context = {
        'request_path': request.path,
        'error_code': '404',
        'error_message': 'Page Not Found',
    }
    
    response = render(request, '404.html', context)
    response.status_code = 404
    return response


def handler500(request):
    """
    Custom 500 error handler.
    
    Args:
        request: HTTP request that resulted in 500
        
    Returns:
        HttpResponseServerError with custom template
    """
    logger.error(
        f"500 Error: {request.path} - "
        f"Method: {request.method} - "
        f"User: {request.user if hasattr(request, 'user') and request.user.is_authenticated else 'Anonymous'}",
        exc_info=True
    )
    
    context = {
        'request_path': request.path,
        'error_code': '500',
        'error_message': 'Internal Server Error',
    }
    
    response = render(request, '500.html', context)
    response.status_code = 500
    return response


def handler403(request, exception=None):
    """
    Custom 403 error handler.
    
    Args:
        request: HTTP request that resulted in 403
        exception: Optional exception that caused the 403
        
    Returns:
        HttpResponseForbidden with custom template
    """
    logger.warning(
        f"403 Error: {request.path} - "
        f"User: {request.user if request.user.is_authenticated else 'Anonymous'}"
    )
    
    context = {
        'request_path': request.path,
        'error_code': '403',
        'error_message': 'Access Forbidden',
    }
    
    response = render(request, '403.html', context)
    response.status_code = 403
    return response


def handler400(request, exception=None):
    """
    Custom 400 error handler.
    
    Args:
        request: HTTP request that resulted in 400
        exception: Optional exception that caused the 400
        
    Returns:
        HttpResponseBadRequest with custom template
    """
    logger.warning(
        f"400 Error: {request.path} - "
        f"User: {request.user if request.user.is_authenticated else 'Anonymous'}"
    )
    
    context = {
        'request_path': request.path,
        'error_code': '400',
        'error_message': 'Bad Request',
    }
    
    response = render(request, '400.html', context)
    response.status_code = 400
    return response
