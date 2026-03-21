"""
Custom error handlers to log exceptions in production
"""
import logging
import traceback

logger = logging.getLogger(__name__)


def custom_500_error(request):
    """Custom 500 error handler that logs the exception"""
    import sys
    exc_info = sys.exc_info()
    if exc_info[0]:
        logger.error(
            'Unhandled exception occurred',
            exc_info=True,
            extra={'request': request}
        )
        logger.error('Exception traceback: ' + traceback.format_exc())
    
    from django.shortcuts import render
    return render(request, '500.html', status=500)


def custom_404_error(request, exception):
    """Custom 404 error handler for pages (not static files)"""
    # Don't render HTML for static/media files
    if request.path.startswith('/static/') or request.path.startswith('/media/'):
        # Let Django return a bare 404 without HTML
        from django.http import HttpResponse
        return HttpResponse(status=404)
    
    # For actual page 404s, show the error page
    logger.warning(f'404 error for path: {request.path}')
    from django.shortcuts import render
    return render(request, '404.html', status=404)


def custom_400_error(request, exception=None):
    """Custom 400 error handler"""
    logger.warning(f'400 error for request: {request.path}', exc_info=True)
    from django.shortcuts import render
    return render(request, '400.html', status=400)
