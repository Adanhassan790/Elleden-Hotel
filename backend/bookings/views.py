from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import logging
import threading

from .models import Booking, Payment
from .forms import BookingForm, GuestBookingForm, PaymentForm
from .emails import send_booking_confirmation
from rooms.models import Room, RoomType
from pages.models import Notification

logger = logging.getLogger(__name__)


class BookingCreateView(CreateView):
    """Public booking form for website visitors"""
    model = Booking
    form_class = GuestBookingForm
    template_name = 'bookings/booking_form.html'
    
    def form_valid(self, form):
        room_type = form.cleaned_data['room_type']
        check_in = form.cleaned_data['check_in_date']
        check_out = form.cleaned_data['check_out_date']
        
        # Find available room of this type
        available_room = Room.objects.filter(
            room_type=room_type,
            status='available',
            is_active=True
        ).exclude(
            bookings__check_in_date__lt=check_out,
            bookings__check_out_date__gt=check_in,
            bookings__status__in=['confirmed', 'checked_in']
        ).first()
        
        if not available_room:
            messages.error(self.request, 'Sorry, no rooms of this type are available for the selected dates.')
            return self.form_invalid(form)
        
        booking = form.save(commit=False)
        booking.room = available_room
        booking.nightly_rate = room_type.base_price
        
        # If user is logged in, associate the booking
        if self.request.user.is_authenticated:
            booking.guest = self.request.user
        
        booking.save()
        
        # Create notification if user is logged in
        if booking.guest:
            Notification.objects.create(
                user=booking.guest,
                title=f'Room Booking Submitted - {booking.booking_reference}',
                message=f'Your booking for {booking.room_type.name} has been submitted. Please proceed to payment.',
                notification_type='booking',
                booking=booking,
                icon='fa-calendar-check',
                link=f'/bookings/confirmation/{booking.id}/'
            )
        
        # Send SMS confirmation in background thread (non-blocking)
        # This prevents worker timeout from SMS hanging
        thread = threading.Thread(target=send_booking_confirmation, args=(booking,), daemon=True)
        thread.start()
        
        messages.success(self.request, f'✅ Booking submitted! Reference: {booking.booking_reference}. SMS confirmation sent to {booking.guest_phone}. Please proceed to payment.')
        # Redirect directly to payment instead of confirmation
        return redirect('bookings:payment', pk=booking.pk)


class BookingConfirmationView(DetailView):
    model = Booking
    template_name = 'bookings/booking_confirmation.html'
    context_object_name = 'booking'


class CustomerBookingListView(LoginRequiredMixin, ListView):
    model = Booking
    template_name = 'bookings/customer_bookings.html'
    context_object_name = 'bookings'
    
    def get_queryset(self):
        return Booking.objects.filter(guest=self.request.user)


class CustomerBookingDetailView(LoginRequiredMixin, DetailView):
    model = Booking
    template_name = 'bookings/customer_booking_detail.html'
    context_object_name = 'booking'
    
    def get_queryset(self):
        return Booking.objects.filter(guest=self.request.user)


@login_required
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk, guest=request.user)
    
    if booking.status in ['pending', 'confirmed']:
        booking.cancel()
        messages.success(request, 'Your booking has been cancelled.')
    else:
        messages.error(request, 'This booking cannot be cancelled.')
    
    return redirect('bookings:customer_list')


def check_availability(request):
    """API-style view to check room availability"""
    room_type_id = request.GET.get('room_type')
    check_in = request.GET.get('check_in')
    check_out = request.GET.get('check_out')
    
    if not all([room_type_id, check_in, check_out]):
        return render(request, 'bookings/availability_result.html', {
            'available': False,
            'message': 'Please provide all required information'
        })
    
    try:
        room_type = RoomType.objects.get(pk=room_type_id, is_active=True)
    except RoomType.DoesNotExist:
        return render(request, 'bookings/availability_result.html', {
            'available': False,
            'message': 'Invalid room type'
        })
    
    available_rooms = Room.objects.filter(
        room_type=room_type,
        status='available',
        is_active=True
    ).exclude(
        bookings__check_in_date__lt=check_out,
        bookings__check_out_date__gt=check_in,
        bookings__status__in=['confirmed', 'checked_in']
    )
    
    return render(request, 'bookings/availability_result.html', {
        'available': available_rooms.exists(),
        'room_type': room_type,
        'count': available_rooms.count()
    })


# ============ MANUAL PAYMENT VIEWS ============

def manual_payment(request, pk):
    """
    Display manual payment instructions for the booking
    Customer pays manually via M-Pesa to the provided paybill number
    """
    from django.conf import settings
    
    booking = get_object_or_404(Booking, pk=pk)
    
    context = {
        'booking': booking,
        'paybill_number': settings.HOTEL_PAYBILL_NUMBER,
        'account_number': settings.HOTEL_ACCOUNT_NUMBER,  # Use actual hotel account number
        'account_name': settings.HOTEL_ACCOUNT_NAME,
        'payment_instruction': settings.PAYMENT_INSTRUCTION_TEXT,
    }
    
    return render(request, 'bookings/manual_payment.html', context)
