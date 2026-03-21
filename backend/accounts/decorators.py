from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps


def hotel_staff_required(view_func):
    """Decorator to check if user is hotel staff (staff, manager, or admin)"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check if user exists and is authenticated
        if not hasattr(request, 'user') or not request.user or not request.user.is_authenticated:
            messages.warning(request, 'Please login to access this page.')
            return redirect('accounts:login')
        
        # Check if user has hotel staff permissions
        if not hasattr(request.user, 'is_hotel_staff') or not request.user.is_hotel_staff:
            messages.error(request, 'You do not have permission to access the admin dashboard.')
            return redirect('dashboard:customer_index')
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def manager_required(view_func):
    """Decorator to check if user is manager or admin"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check if user exists and is authenticated
        if not hasattr(request, 'user') or not request.user or not request.user.is_authenticated:
            messages.warning(request, 'Please login to access this page.')
            return redirect('accounts:login')
        
        # Check if user has manager permissions
        if not hasattr(request.user, 'is_manager') or not request.user.is_manager:
            messages.error(request, 'You need manager privileges to access this page.')
            return redirect('dashboard:admin_index')
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def customer_required(view_func):
    """Decorator to ensure user is a customer (not staff)"""
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check if user exists and is authenticated
        if not hasattr(request, 'user') or not request.user or not request.user.is_authenticated:
            messages.warning(request, 'Please login to access this page.')
            return redirect('accounts:login')
        
        # Staff can also view customer pages but customers can't view staff pages
        return view_func(request, *args, **kwargs)
    return _wrapped_view
