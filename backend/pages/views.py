from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from rooms.models import RoomType
from .forms import ContactForm, RestaurantReservationForm, ConferenceBookingForm, CateringInquiryForm


def home(request):
    """Homepage view"""
    room_types = RoomType.objects.all()[:4]
    context = {
        'room_types': room_types,
    }
    return render(request, 'pages/home.html', context)


def about(request):
    """About page view"""
    return render(request, 'pages/about.html')


def rooms(request):
    """Rooms page view"""
    room_types = RoomType.objects.all()
    context = {
        'room_types': room_types,
    }
    return render(request, 'pages/rooms.html', context)


def restaurant(request):
    """Restaurant page view with reservation form"""
    if request.method == 'POST':
        form = RestaurantReservationForm(request.POST)
        if form.is_valid():
            reservation = form.save()
            
            # Send confirmation email
            try:
                subject = f'Restaurant Reservation Confirmation - {reservation.date}'
                html_message = render_to_string('emails/restaurant_reservation.html', {
                    'reservation': reservation,
                })
                send_mail(
                    subject=subject,
                    message='',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[reservation.email],
                    html_message=html_message,
                    fail_silently=True,
                )
                # Notify hotel staff
                send_mail(
                    subject=f'New Restaurant Reservation - {reservation.name}',
                    message=f'New reservation from {reservation.name} for {reservation.guests} guests on {reservation.date} at {reservation.time}.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.DEFAULT_FROM_EMAIL],
                    fail_silently=True,
                )
            except Exception:
                pass
            
            messages.success(request, 'Your reservation has been submitted! We will confirm shortly.')
            return redirect('pages:restaurant')
    else:
        form = RestaurantReservationForm()
    
    return render(request, 'pages/restaurant.html', {'form': form})


def conference(request):
    """Conference page view with booking form"""
    if request.method == 'POST':
        form = ConferenceBookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            
            # Send confirmation email
            try:
                subject = f'Conference Booking Request Received - {booking.event_date}'
                html_message = render_to_string('emails/conference_booking.html', {
                    'booking': booking,
                })
                send_mail(
                    subject=subject,
                    message='',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[booking.email],
                    html_message=html_message,
                    fail_silently=True,
                )
                # Notify hotel staff
                send_mail(
                    subject=f'New Conference Booking - {booking.organization_name}',
                    message=f'New conference booking from {booking.organization_name} for {booking.attendees} attendees on {booking.event_date}.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.DEFAULT_FROM_EMAIL],
                    fail_silently=True,
                )
            except Exception:
                pass
            
            messages.success(request, 'Your conference booking request has been submitted! Our team will contact you shortly.')
            return redirect('pages:conference')
    else:
        form = ConferenceBookingForm()
    
    return render(request, 'pages/conference.html', {'form': form})


def catering(request):
    """Catering page view with inquiry form"""
    if request.method == 'POST':
        form = CateringInquiryForm(request.POST)
        if form.is_valid():
            inquiry = form.save()
            
            # Send confirmation email
            try:
                subject = f'Catering Inquiry Received - {inquiry.event_date}'
                html_message = render_to_string('emails/catering_inquiry.html', {
                    'inquiry': inquiry,
                })
                send_mail(
                    subject=subject,
                    message='',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[inquiry.email],
                    html_message=html_message,
                    fail_silently=True,
                )
                # Notify hotel staff
                send_mail(
                    subject=f'New Catering Inquiry - {inquiry.name}',
                    message=f'New catering inquiry from {inquiry.name} for {inquiry.guest_count} guests on {inquiry.event_date}.',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.DEFAULT_FROM_EMAIL],
                    fail_silently=True,
                )
            except Exception:
                pass
            
            messages.success(request, 'Your catering inquiry has been submitted! We will send you a quote shortly.')
            return redirect('pages:catering')
    else:
        form = CateringInquiryForm()
    
    return render(request, 'pages/catering.html', {'form': form})


def contact(request):
    """Contact page view with contact form"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            message = form.save()
            
            # Send confirmation email
            try:
                subject = f'Thank You for Contacting Elleden Hotel'
                html_message = render_to_string('emails/contact_confirmation.html', {
                    'message': message,
                })
                send_mail(
                    subject=subject,
                    message='',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[message.email],
                    html_message=html_message,
                    fail_silently=True,
                )
                # Notify hotel staff
                send_mail(
                    subject=f'New Contact Message - {message.get_subject_display()}',
                    message=f'New message from {message.full_name} ({message.email}):\n\n{message.message}',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.DEFAULT_FROM_EMAIL],
                    fail_silently=True,
                )
            except Exception:
                pass
            
            messages.success(request, 'Thank you for your message! We will get back to you soon.')
            return redirect('pages:contact')
    else:
        form = ContactForm()
    
    return render(request, 'pages/contact.html', {'form': form})
