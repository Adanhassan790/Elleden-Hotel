from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Sum, Count, Q, Avg
from django.db.models.functions import TruncDate, TruncMonth
from django.http import JsonResponse
from datetime import timedelta
import json

from accounts.models import User
from accounts.decorators import hotel_staff_required
from rooms.models import Room, RoomType
from bookings.models import Booking, Payment, MpesaTransaction
from pages.models import (
    RestaurantReservation, ConferenceBooking, CateringOrder,
    CateringPackage, ServicePayment, ServiceMpesaTransaction
)


def home_redirect(request):
    """Redirect home based on user type"""
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.user_type in ['admin', 'manager', 'staff']:
            return redirect('dashboard:admin_index')
        return redirect('dashboard:customer_index')
    return redirect('accounts:login')


@hotel_staff_required
def admin_dashboard(request):
    """Main admin dashboard with comprehensive analytics"""
    today = timezone.now().date()
    first_day_of_month = today.replace(day=1)
    thirty_days_ago = today - timedelta(days=30)
    seven_days_ago = today - timedelta(days=7)
    
    # ========== ROOM STATISTICS ==========
    total_rooms = Room.objects.filter(is_active=True).count()
    available_rooms = Room.objects.filter(is_active=True, status='available').count()
    occupied_rooms = Room.objects.filter(is_active=True, status='occupied').count()
    occupancy_rate = (occupied_rooms / total_rooms * 100) if total_rooms > 0 else 0
    
    # Room bookings
    total_room_bookings = Booking.objects.count()
    pending_room_bookings = Booking.objects.filter(status='pending').count()
    todays_checkins = Booking.objects.filter(check_in_date=today, status='confirmed').count()
    todays_checkouts = Booking.objects.filter(check_out_date=today, status='checked_in').count()
    
    # ========== CONFERENCE STATISTICS ==========
    total_conference_bookings = ConferenceBooking.objects.count()
    pending_conferences = ConferenceBooking.objects.filter(status='pending').count()
    upcoming_conferences = ConferenceBooking.objects.filter(
        event_date__gte=today, status='confirmed'
    ).count()
    
    # ========== CATERING STATISTICS ==========
    total_catering_orders = CateringOrder.objects.count()
    pending_catering = CateringOrder.objects.filter(status='pending').count()
    upcoming_catering = CateringOrder.objects.filter(
        event_date__gte=today, status__in=['confirmed', 'preparing']
    ).count()
    
    # ========== RESTAURANT STATISTICS ==========
    total_reservations = RestaurantReservation.objects.count()
    todays_reservations = RestaurantReservation.objects.filter(date=today).count()
    upcoming_reservations = RestaurantReservation.objects.filter(
        date__gte=today, status='confirmed'
    ).count()
    
    # ========== REVENUE STATISTICS ==========
    # Room payments
    room_revenue_month = Payment.objects.filter(
        created_at__date__gte=first_day_of_month
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    room_revenue_total = Payment.objects.aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    # Service payments (conference + catering)
    service_revenue_month = ServicePayment.objects.filter(
        created_at__date__gte=first_day_of_month
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    service_revenue_total = ServicePayment.objects.aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    # Total revenue
    total_revenue_month = room_revenue_month + service_revenue_month
    total_revenue_all = room_revenue_total + service_revenue_total
    
    # ========== M-PESA STATISTICS ==========
    mpesa_room_count = MpesaTransaction.objects.filter(status='completed').count()
    mpesa_service_count = ServiceMpesaTransaction.objects.filter(status='completed').count()
    total_mpesa_transactions = mpesa_room_count + mpesa_service_count
    
    mpesa_room_amount = MpesaTransaction.objects.filter(
        status='completed'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    mpesa_service_amount = ServiceMpesaTransaction.objects.filter(
        status='completed'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    total_mpesa_amount = mpesa_room_amount + mpesa_service_amount
    
    # ========== CHART DATA ==========
    # Revenue trend (last 30 days)
    daily_room_revenue = Payment.objects.filter(
        created_at__date__gte=thirty_days_ago
    ).annotate(date=TruncDate('created_at')).values('date').annotate(
        total=Sum('amount')
    ).order_by('date')
    
    daily_service_revenue = ServicePayment.objects.filter(
        created_at__date__gte=thirty_days_ago
    ).annotate(date=TruncDate('created_at')).values('date').annotate(
        total=Sum('amount')
    ).order_by('date')
    
    # Combine revenue data
    revenue_data = {}
    for item in daily_room_revenue:
        date_str = item['date'].strftime('%Y-%m-%d')
        revenue_data[date_str] = {'rooms': float(item['total']), 'services': 0}
    
    for item in daily_service_revenue:
        date_str = item['date'].strftime('%Y-%m-%d')
        if date_str in revenue_data:
            revenue_data[date_str]['services'] = float(item['total'])
        else:
            revenue_data[date_str] = {'rooms': 0, 'services': float(item['total'])}
    
    # Bookings by service type (for pie chart)
    service_distribution = [
        {'name': 'Room Bookings', 'value': total_room_bookings},
        {'name': 'Conference', 'value': total_conference_bookings},
        {'name': 'Catering', 'value': total_catering_orders},
        {'name': 'Restaurant', 'value': total_reservations},
    ]
    
    # ========== RECENT ACTIVITY ==========
    recent_room_bookings = Booking.objects.select_related('room_type').order_by('-created_at')[:5]
    recent_conferences = ConferenceBooking.objects.order_by('-created_at')[:5]
    recent_catering = CateringOrder.objects.order_by('-created_at')[:5]
    recent_reservations = RestaurantReservation.objects.order_by('-created_at')[:5]
    
    # Recent payments
    recent_room_payments = Payment.objects.select_related('booking').order_by('-created_at')[:5]
    recent_service_payments = ServicePayment.objects.order_by('-created_at')[:5]
    
    # ========== ITEMS REQUIRING ATTENTION ==========
    attention_room_bookings = Booking.objects.filter(
        Q(status='pending') | 
        Q(check_in_date=today, status='confirmed') |
        Q(check_out_date=today, status='checked_in')
    ).order_by('check_in_date')[:5]
    
    attention_conferences = ConferenceBooking.objects.filter(
        Q(status='pending') | Q(event_date=today, status='confirmed')
    ).order_by('event_date')[:5]
    
    attention_catering = CateringOrder.objects.filter(
        Q(status='pending') | Q(event_date=today, status='confirmed')
    ).order_by('event_date')[:5]
    
    context = {
        # Room stats
        'total_rooms': total_rooms,
        'available_rooms': available_rooms,
        'occupied_rooms': occupied_rooms,
        'occupancy_rate': round(occupancy_rate, 1),
        'total_room_bookings': total_room_bookings,
        'pending_room_bookings': pending_room_bookings,
        'todays_checkins': todays_checkins,
        'todays_checkouts': todays_checkouts,
        
        # Conference stats
        'total_conference_bookings': total_conference_bookings,
        'pending_conferences': pending_conferences,
        'upcoming_conferences': upcoming_conferences,
        
        # Catering stats
        'total_catering_orders': total_catering_orders,
        'pending_catering': pending_catering,
        'upcoming_catering': upcoming_catering,
        
        # Restaurant stats
        'total_reservations': total_reservations,
        'todays_reservations': todays_reservations,
        'upcoming_reservations': upcoming_reservations,
        
        # Revenue stats
        'room_revenue_month': room_revenue_month,
        'service_revenue_month': service_revenue_month,
        'total_revenue_month': total_revenue_month,
        'total_revenue_all': total_revenue_all,
        
        # M-Pesa stats
        'total_mpesa_transactions': total_mpesa_transactions,
        'total_mpesa_amount': total_mpesa_amount,
        
        # Chart data
        'revenue_chart_data': json.dumps(revenue_data),
        'service_distribution': json.dumps(service_distribution),
        
        # Recent activity
        'recent_room_bookings': recent_room_bookings,
        'recent_conferences': recent_conferences,
        'recent_catering': recent_catering,
        'recent_reservations': recent_reservations,
        'recent_room_payments': recent_room_payments,
        'recent_service_payments': recent_service_payments,
        
        # Attention items
        'attention_room_bookings': attention_room_bookings,
        'attention_conferences': attention_conferences,
        'attention_catering': attention_catering,
    }
    
    return render(request, 'dashboard/admin/index.html', context)


@hotel_staff_required
def booking_management(request):
    """View and manage all room bookings"""
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


@hotel_staff_required
def booking_detail(request, pk):
    """View and edit a single room booking"""
    booking = get_object_or_404(Booking.objects.select_related('room', 'room_type', 'guest'), pk=pk)
    payments = booking.payments.all()
    
    context = {
        'booking': booking,
        'payments': payments,
    }
    
    return render(request, 'dashboard/admin/booking_detail.html', context)


@hotel_staff_required
def booking_action(request, pk, action):
    """Perform actions on bookings"""
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


@hotel_staff_required
def room_management(request):
    """View and manage rooms"""
    rooms = Room.objects.select_related('room_type').order_by('room_number')
    room_types = RoomType.objects.all()
    
    context = {
        'rooms': rooms,
        'room_types': room_types,
    }
    
    return render(request, 'dashboard/admin/rooms.html', context)


@hotel_staff_required
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


@hotel_staff_required
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


@hotel_staff_required  
def reports_dashboard(request):
    """View reports and analytics"""
    today = timezone.now().date()
    thirty_days_ago = today - timedelta(days=30)
    
    daily_revenue = Payment.objects.filter(
        created_at__date__gte=thirty_days_ago
    ).values('created_at__date').annotate(
        total=Sum('amount')
    ).order_by('created_at__date')
    
    bookings_by_status = Booking.objects.values('status').annotate(count=Count('id'))
    
    revenue_by_room_type = Booking.objects.filter(status='checked_out').values(
        'room_type__name'
    ).annotate(total=Sum('total_amount'))
    
    context = {
        'daily_revenue': list(daily_revenue),
        'bookings_by_status': list(bookings_by_status),
        'revenue_by_room_type': list(revenue_by_room_type),
    }
    
    return render(request, 'dashboard/admin/reports.html', context)


# ========== SERVICE MANAGEMENT VIEWS ==========

@hotel_staff_required
def conference_management(request):
    """View and manage all conference bookings"""
    status_filter = request.GET.get('status', '')
    payment_filter = request.GET.get('payment', '')
    search = request.GET.get('search', '')
    
    bookings = ConferenceBooking.objects.all()
    
    if status_filter:
        bookings = bookings.filter(status=status_filter)
    
    if payment_filter:
        bookings = bookings.filter(payment_status=payment_filter)
    
    if search:
        bookings = bookings.filter(
            Q(booking_reference__icontains=search) |
            Q(organization_name__icontains=search) |
            Q(contact_person__icontains=search) |
            Q(email__icontains=search)
        )
    
    bookings = bookings.order_by('-created_at')[:100]
    
    context = {
        'bookings': bookings,
        'status_choices': ConferenceBooking.STATUS_CHOICES,
        'payment_choices': ConferenceBooking.PAYMENT_STATUS,
        'current_status': status_filter,
        'current_payment': payment_filter,
        'search_query': search,
    }
    
    return render(request, 'dashboard/admin/conferences.html', context)


@hotel_staff_required
def conference_detail(request, pk):
    """View conference booking details"""
    booking = get_object_or_404(ConferenceBooking, pk=pk)
    payments = booking.payments.all()
    
    context = {
        'booking': booking,
        'payments': payments,
    }
    
    return render(request, 'dashboard/admin/conference_detail.html', context)


@hotel_staff_required
def conference_action(request, pk, action):
    """Perform actions on conference bookings"""
    booking = get_object_or_404(ConferenceBooking, pk=pk)
    
    if action == 'confirm' and booking.status == 'pending':
        booking.status = 'confirmed'
        booking.save()
        messages.success(request, f'Conference booking {booking.booking_reference} confirmed.')
    
    elif action == 'complete' and booking.status == 'confirmed':
        booking.status = 'completed'
        booking.save()
        messages.success(request, f'Conference booking {booking.booking_reference} marked as completed.')
    
    elif action == 'cancel' and booking.status in ['pending', 'confirmed']:
        booking.status = 'cancelled'
        booking.save()
        messages.success(request, f'Conference booking {booking.booking_reference} cancelled.')
    
    else:
        messages.error(request, 'Invalid action for this booking status.')
    
    return redirect('dashboard:conference_detail', pk=pk)


@hotel_staff_required
def catering_management(request):
    """View and manage all catering orders"""
    status_filter = request.GET.get('status', '')
    payment_filter = request.GET.get('payment', '')
    search = request.GET.get('search', '')
    
    orders = CateringOrder.objects.select_related('package')
    
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    if payment_filter:
        orders = orders.filter(payment_status=payment_filter)
    
    if search:
        orders = orders.filter(
            Q(booking_reference__icontains=search) |
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(venue_address__icontains=search)
        )
    
    orders = orders.order_by('-created_at')[:100]
    packages = CateringPackage.objects.all()
    
    context = {
        'orders': orders,
        'packages': packages,
        'status_choices': CateringOrder.STATUS_CHOICES,
        'payment_choices': CateringOrder.PAYMENT_STATUS,
        'current_status': status_filter,
        'current_payment': payment_filter,
        'search_query': search,
    }
    
    return render(request, 'dashboard/admin/catering.html', context)


@hotel_staff_required
def catering_detail(request, pk):
    """View catering order details"""
    order = get_object_or_404(CateringOrder.objects.select_related('package'), pk=pk)
    payments = order.payments.all()
    
    context = {
        'order': order,
        'payments': payments,
    }
    
    return render(request, 'dashboard/admin/catering_detail.html', context)


@hotel_staff_required
def catering_action(request, pk, action):
    """Perform actions on catering orders"""
    order = get_object_or_404(CateringOrder, pk=pk)
    
    valid_actions = {
        'confirm': ('pending', 'confirmed'),
        'preparing': ('confirmed', 'preparing'),
        'deliver': ('preparing', 'delivered'),
        'complete': ('delivered', 'completed'),
        'cancel': (['pending', 'confirmed'], 'cancelled'),
    }
    
    if action in valid_actions:
        required_status, new_status = valid_actions[action]
        
        if isinstance(required_status, list):
            valid = order.status in required_status
        else:
            valid = order.status == required_status
        
        if valid:
            order.status = new_status
            order.save()
            messages.success(request, f'Catering order {order.booking_reference} updated to {order.get_status_display()}.')
        else:
            messages.error(request, 'Invalid action for this order status.')
    else:
        messages.error(request, 'Invalid action.')
    
    return redirect('dashboard:catering_detail', pk=pk)


@hotel_staff_required
def restaurant_management(request):
    """View and manage all restaurant reservations"""
    status_filter = request.GET.get('status', '')
    date_filter = request.GET.get('date', '')
    search = request.GET.get('search', '')
    
    reservations = RestaurantReservation.objects.all()
    
    if status_filter:
        reservations = reservations.filter(status=status_filter)
    
    if date_filter:
        reservations = reservations.filter(date=date_filter)
    
    if search:
        reservations = reservations.filter(
            Q(booking_reference__icontains=search) |
            Q(name__icontains=search) |
            Q(email__icontains=search) |
            Q(phone__icontains=search)
        )
    
    reservations = reservations.order_by('-date', '-time')[:100]
    
    context = {
        'reservations': reservations,
        'status_choices': RestaurantReservation.STATUS_CHOICES,
        'current_status': status_filter,
        'current_date': date_filter,
        'search_query': search,
    }
    
    return render(request, 'dashboard/admin/restaurant.html', context)


@hotel_staff_required
def restaurant_action(request, pk, action):
    """Perform actions on restaurant reservations"""
    reservation = get_object_or_404(RestaurantReservation, pk=pk)
    
    if action == 'confirm' and reservation.status == 'pending':
        reservation.status = 'confirmed'
        reservation.save()
        messages.success(request, f'Reservation {reservation.booking_reference} confirmed.')
    
    elif action == 'complete' and reservation.status == 'confirmed':
        reservation.status = 'completed'
        reservation.save()
        messages.success(request, f'Reservation {reservation.booking_reference} marked as completed.')
    
    elif action == 'cancel' and reservation.status in ['pending', 'confirmed']:
        reservation.status = 'cancelled'
        reservation.save()
        messages.success(request, f'Reservation {reservation.booking_reference} cancelled.')
    
    else:
        messages.error(request, 'Invalid action for this reservation status.')
    
    return redirect('dashboard:restaurant')


@hotel_staff_required
def payments_management(request):
    """View all payments across services"""
    room_payments = Payment.objects.select_related('booking').order_by('-created_at')[:50]
    service_payments = ServicePayment.objects.order_by('-created_at')[:50]
    room_mpesa = MpesaTransaction.objects.order_by('-created_at')[:30]
    service_mpesa = ServiceMpesaTransaction.objects.order_by('-created_at')[:30]
    
    context = {
        'room_payments': room_payments,
        'service_payments': service_payments,
        'room_mpesa': room_mpesa,
        'service_mpesa': service_mpesa,
    }
    
    return render(request, 'dashboard/admin/payments.html', context)


@hotel_staff_required
def api_dashboard_stats(request):
    """API endpoint for real-time dashboard stats"""
    today = timezone.now().date()
    
    stats = {
        'available_rooms': Room.objects.filter(is_active=True, status='available').count(),
        'pending_bookings': Booking.objects.filter(status='pending').count(),
        'pending_conferences': ConferenceBooking.objects.filter(status='pending').count(),
        'pending_catering': CateringOrder.objects.filter(status='pending').count(),
        'todays_checkins': Booking.objects.filter(check_in_date=today, status='confirmed').count(),
        'todays_reservations': RestaurantReservation.objects.filter(date=today).count(),
    }
    
    return JsonResponse(stats)


# Customer Dashboard Views
@login_required
def customer_dashboard(request):
    """Customer's personal dashboard with all their bookings and services"""
    user = request.user
    
    # Redirect staff to admin dashboard
    if user.is_hotel_staff:
        return redirect('dashboard:admin_index')
    
    # Room Bookings
    bookings = Booking.objects.filter(guest=user).order_by('-created_at')
    active_bookings = bookings.filter(status__in=['pending', 'confirmed', 'checked_in']).count()
    completed_bookings = bookings.filter(status='checked_out').count()
    recent_bookings = bookings[:5]
    
    # Restaurant Reservations (filter by email)
    restaurant_reservations = RestaurantReservation.objects.filter(
        email=user.email
    ).order_by('-created_at')
    upcoming_reservations = restaurant_reservations.filter(
        status__in=['pending', 'confirmed']
    ).count()
    
    # Conference Bookings (filter by email)
    conference_bookings = ConferenceBooking.objects.filter(
        email=user.email
    ).order_by('-created_at')
    upcoming_conferences = conference_bookings.filter(
        status__in=['pending', 'confirmed']
    ).count()
    
    # Catering Orders (filter by email)
    catering_orders = CateringOrder.objects.filter(
        email=user.email
    ).order_by('-created_at')
    upcoming_catering = catering_orders.filter(
        status__in=['pending', 'confirmed', 'preparing']
    ).count()
    
    context = {
        # Room bookings
        'recent_bookings': recent_bookings,
        'total_bookings': bookings.count(),
        'active_bookings': active_bookings,
        'completed_bookings': completed_bookings,
        
        # Restaurant
        'restaurant_reservations': restaurant_reservations[:3],
        'total_reservations': restaurant_reservations.count(),
        'upcoming_reservations': upcoming_reservations,
        
        # Conference
        'conference_bookings': conference_bookings[:3],
        'total_conferences': conference_bookings.count(),
        'upcoming_conferences': upcoming_conferences,
        
        # Catering
        'catering_orders': catering_orders[:3],
        'total_catering': catering_orders.count(),
        'upcoming_catering': upcoming_catering,
    }
    
    return render(request, 'dashboard/customer/index.html', context)

