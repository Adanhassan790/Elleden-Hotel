from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum, Count, Q
from django.http import JsonResponse
from datetime import timedelta

from accounts.models import User
from rooms.models import Room, RoomType
from bookings.models import Booking, Payment


def home_redirect(request):
    """Redirect home based on user type"""
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.user_type in ['admin', 'manager', 'staff']:
            return redirect('dashboard:admin_index')
        return redirect('dashboard:customer_index')
    return redirect('accounts:login')


@staff_member_required
def admin_dashboard(request):
    """Main admin dashboard with overview stats"""
    today = timezone.now().date()
    
    # Room statistics
    total_rooms = Room.objects.filter(is_active=True).count()
    available_rooms = Room.objects.filter(is_active=True, status='available').count()
    occupied_rooms = Room.objects.filter(is_active=True, status='occupied').count()
    
    # Booking statistics
    todays_checkins = Booking.objects.filter(
        check_in_date=today, 
        status='confirmed'
    ).count()
    
    todays_checkouts = Booking.objects.filter(
        check_out_date=today, 
        status='checked_in'
    ).count()
    
    pending_bookings = Booking.objects.filter(status='pending').count()
    
    # Current occupancy rate
    occupancy_rate = (occupied_rooms / total_rooms * 100) if total_rooms > 0 else 0
    
    # Revenue this month
    first_day_of_month = today.replace(day=1)
    monthly_revenue = Payment.objects.filter(
        created_at__date__gte=first_day_of_month
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Recent bookings
    recent_bookings = Booking.objects.select_related('room', 'room_type').order_by('-created_at')[:10]
    
    # Bookings requiring attention
    attention_bookings = Booking.objects.filter(
        Q(status='pending') | 
        Q(check_in_date=today, status='confirmed') |
        Q(check_out_date=today, status='checked_in')
    ).order_by('check_in_date')[:10]
    
    context = {
        'total_rooms': total_rooms,
        'available_rooms': available_rooms,
        'occupied_rooms': occupied_rooms,
        'occupancy_rate': round(occupancy_rate, 1),
        'todays_checkins': todays_checkins,
        'todays_checkouts': todays_checkouts,
        'pending_bookings': pending_bookings,
        'monthly_revenue': monthly_revenue,
        'recent_bookings': recent_bookings,
        'attention_bookings': attention_bookings,
    }
    
    return render(request, 'dashboard/admin/index.html', context)


@staff_member_required
def booking_management(request):
    """View and manage all bookings"""
    status_filter = request.GET.get('status', '')
    date_filter = request.GET.get('date', '')
    search = request.GET.get('search', '')
    
    bookings = Booking.objects.select_related('room', 'room_type', 'guest')
    
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    
    if date_filter:
        bookings = bookings.filter(check_in_date=date_filter)
    
    if search:
        bookings = bookings.filter(
            Q(booking_reference__icontains=search) |
            Q(guest_name__icontains=search) |
            Q(guest_email__icontains=search) |
            Q(guest_phone__icontains=search)
        )
    
    bookings = bookings.order_by('-created_at')[:100]
    
    context = {
        'bookings': bookings,
        'status_choices': Booking.STATUS_CHOICES,
        'current_status': status_filter,
        'current_date': date_filter,
        'search_query': search,
    }
    
    return render(request, 'dashboard/admin/bookings.html', context)


@staff_member_required
def booking_detail(request, pk):
    """View and edit a single booking"""
    booking = get_object_or_404(Booking.objects.select_related('room', 'room_type', 'guest'), pk=pk)
    payments = booking.payments.all()
    
    context = {
        'booking': booking,
        'payments': payments,
    }
    
    return render(request, 'dashboard/admin/booking_detail.html', context)


@staff_member_required
def booking_action(request, pk, action):
    """Perform actions on bookings (check-in, check-out, confirm, cancel)"""
    booking = get_object_or_404(Booking, pk=pk)
    
    if action == 'confirm' and booking.status == 'pending':
        booking.confirm()
        messages.success(request, f'Booking {booking.booking_reference} confirmed.')
    
    elif action == 'checkin' and booking.status == 'confirmed':
        booking.check_in()
        messages.success(request, f'Guest checked in to Room {booking.room.room_number}.')
    
    elif action == 'checkout' and booking.status == 'checked_in':
        booking.check_out()
        messages.success(request, f'Guest checked out from Room {booking.room.room_number}.')
    
    elif action == 'cancel' and booking.status in ['pending', 'confirmed']:
        booking.cancel()
        messages.success(request, f'Booking {booking.booking_reference} cancelled.')
    
    else:
        messages.error(request, 'Invalid action for this booking status.')
    
    return redirect('dashboard:booking_detail', pk=pk)


@staff_member_required
def room_management(request):
    """View and manage rooms"""
    rooms = Room.objects.select_related('room_type').order_by('room_number')
    room_types = RoomType.objects.all()
    
    context = {
        'rooms': rooms,
        'room_types': room_types,
    }
    
    return render(request, 'dashboard/admin/rooms.html', context)


@staff_member_required
def room_status_update(request, pk, status):
    """Update room status"""
    room = get_object_or_404(Room, pk=pk)
    
    if status in dict(Room.STATUS_CHOICES):
        room.status = status
        room.save()
        messages.success(request, f'Room {room.room_number} status updated to {room.get_status_display()}.')
    else:
        messages.error(request, 'Invalid status.')
    
    return redirect('dashboard:rooms')


@staff_member_required
def guest_management(request):
    """View all registered customers"""
    guests = User.objects.filter(user_type='customer').order_by('-date_joined')
    
    search = request.GET.get('search', '')
    if search:
        guests = guests.filter(
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search) |
            Q(email__icontains=search) |
            Q(phone__icontains=search)
        )
    
    context = {
        'guests': guests,
        'search_query': search,
    }
    
    return render(request, 'dashboard/admin/guests.html', context)


@staff_member_required  
def reports_dashboard(request):
    """View reports and analytics"""
    today = timezone.now().date()
    
    # Last 30 days revenue
    thirty_days_ago = today - timedelta(days=30)
    daily_revenue = Payment.objects.filter(
        created_at__date__gte=thirty_days_ago
    ).values('created_at__date').annotate(
        total=Sum('amount')
    ).order_by('created_at__date')
    
    # Bookings by status
    bookings_by_status = Booking.objects.values('status').annotate(
        count=Count('id')
    )
    
    # Revenue by room type
    revenue_by_room_type = Booking.objects.filter(
        status='checked_out'
    ).values('room_type__name').annotate(
        total=Sum('total_amount')
    )
    
    context = {
        'daily_revenue': list(daily_revenue),
        'bookings_by_status': list(bookings_by_status),
        'revenue_by_room_type': list(revenue_by_room_type),
    }
    
    return render(request, 'dashboard/admin/reports.html', context)


# Customer Dashboard Views
@login_required
def customer_dashboard(request):
    """Customer's personal dashboard"""
    user = request.user
    
    # Get customer's bookings
    bookings = Booking.objects.filter(guest=user).order_by('-created_at')
    active_bookings = bookings.filter(status__in=['pending', 'confirmed', 'checked_in']).count()
    completed_bookings = bookings.filter(status='checked_out').count()
    
    # Recent bookings
    recent_bookings = bookings[:5]
    
    context = {
        'recent_bookings': recent_bookings,
        'total_bookings': bookings.count(),
        'active_bookings': active_bookings,
        'completed_bookings': completed_bookings,
    }
    
    return render(request, 'dashboard/customer/index.html', context)
