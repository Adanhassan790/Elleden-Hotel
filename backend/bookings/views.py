from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from .models import Booking, Payment
from .forms import BookingForm, GuestBookingForm, PaymentForm
from .emails import send_booking_confirmation_email
from rooms.models import Room, RoomType


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
        
        # Send confirmation email
        send_booking_confirmation_email(booking)
        
        messages.success(self.request, f'Booking submitted successfully! Your reference: {booking.booking_reference}')
        return redirect('bookings:confirmation', pk=booking.pk)


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
