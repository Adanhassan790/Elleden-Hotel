from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
import logging
import threading

from rooms.models import RoomType
from .forms import (ContactForm, RestaurantReservationForm, ConferenceBookingForm, 
                   CateringInquiryForm, CateringOrderForm)
from .models import (RestaurantReservation, ConferenceBooking, CateringOrder, 
                    CateringPackage, ServicePayment)
from .notifications import (send_restaurant_reservation_sms, send_conference_booking_sms,
                           send_catering_order_sms, send_service_payment_sms, 
                           send_contact_response_sms)

logger = logging.getLogger(__name__)


def home(request):
    """Homepage view - redirects staff to admin dashboard"""
    # Safely check if user is authenticated and has hotel staff permission
    if (hasattr(request, 'user') and request.user and 
        request.user.is_authenticated and 
        hasattr(request.user, 'is_hotel_staff') and 
        request.user.is_hotel_staff):
        return redirect('dashboard:admin_index')
    
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
            try:
                reservation = form.save()
                
                # Send SMS confirmation in background thread (non-blocking)
                # This prevents worker timeout from SMS hanging
                def send_notifications():
                    """Send SMS and email notifications safely in background"""
                    try:
                        send_restaurant_reservation_sms(reservation)
                    except Exception as e:
                        logger.error(f"Error sending SMS: {e}", exc_info=True)
                    
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
                    except Exception as e:
                        logger.error(f"Error sending email: {e}", exc_info=True)
                
                thread = threading.Thread(target=send_notifications, daemon=True)
                thread.start()
                
                messages.success(request, f'✅ Reservation confirmed! Reference: {reservation.booking_reference}. SMS confirmation sent to {reservation.phone}. You will receive further details shortly.')
                return redirect('pages:restaurant_confirmation', pk=reservation.pk)
            
            except Exception as e:
                logger.error(f"Error creating restaurant reservation: {e}", exc_info=True)
                messages.error(request, f'❌ Error creating reservation: {str(e)}')
                return render(request, 'pages/restaurant.html', {'form': form})
    else:
        form = RestaurantReservationForm()
    
    return render(request, 'pages/restaurant.html', {'form': form})


def restaurant_confirmation(request, pk):
    """Restaurant reservation confirmation page"""
    reservation = get_object_or_404(RestaurantReservation, pk=pk)
    return render(request, 'pages/restaurant_confirmation.html', {'reservation': reservation})


def conference(request):
    """Conference page view with booking form"""
    if request.method == 'POST':
        form = ConferenceBookingForm(request.POST)
        if form.is_valid():
            try:
                booking = form.save()
                
                # Send SMS confirmation in background thread (non-blocking)
                # This prevents worker timeout from SMS hanging
                thread = threading.Thread(target=send_conference_booking_sms, args=(booking,), daemon=True)
                thread.start()
                
                # Send email as backup
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
                
                messages.success(request, f'Conference booking received! Reference: {booking.booking_reference}. SMS confirmation sent to {booking.phone}. Our team will contact you shortly.')
                return redirect('pages:conference_confirmation', pk=booking.pk)
            except Exception as e:
                logger.error(f"Error creating conference booking: {e}", exc_info=True)
                messages.error(request, f'Error creating booking: {str(e)}')
                return render(request, 'pages/conference.html', {'form': form})
        else:
            # Form is invalid, return with form errors
            return render(request, 'pages/conference.html', {'form': form})
    else:
        form = ConferenceBookingForm()
    
    return render(request, 'pages/conference.html', {'form': form})


def conference_confirmation(request, pk):
    """Conference booking confirmation page with payment option"""
    booking = get_object_or_404(ConferenceBooking, pk=pk)
    return render(request, 'pages/conference_confirmation.html', {'booking': booking})


def catering(request):
    """Catering page view with package selection and order form"""
    packages = CateringPackage.objects.filter(is_active=True)
    
    if request.method == 'POST':
        form = CateringOrderForm(request.POST)
        if form.is_valid():
            try:
                order = form.save()
                
                # Send SMS confirmation in background thread (non-blocking)
                # This prevents worker timeout from SMS hanging
                thread = threading.Thread(target=send_catering_order_sms, args=(order,), daemon=True)
                thread.start()
                
                # Send email as backup
                try:
                    subject = f'Catering Order Received - {order.booking_reference}'
                    html_message = render_to_string('emails/catering_inquiry.html', {
                        'order': order,
                    })
                    send_mail(
                        subject=subject,
                        message='',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[order.email],
                        html_message=html_message,
                        fail_silently=True,
                    )
                    # Notify hotel staff
                    send_mail(
                        subject=f'New Catering Order - {order.booking_reference}',
                        message=f'New catering order from {order.name} for {order.guest_count} guests on {order.event_date}. Total: KES {order.total_amount}',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        recipient_list=[settings.DEFAULT_FROM_EMAIL],
                        fail_silently=True,
                    )
                except Exception:
                    pass
                
                messages.success(request, f'Catering order received! Reference: {order.booking_reference}. SMS confirmation sent to {order.phone}. We will respond with pricing within 24 hours.')
                return redirect('pages:catering_confirmation', pk=order.pk)
            except Exception as e:
                logger.error(f"Error creating catering order: {e}", exc_info=True)
                messages.error(request, f'Error creating catering order: {str(e)}')
                return render(request, 'pages/catering.html', {'form': form, 'packages': packages})
        else:
            # Form is invalid, return with form errors
            return render(request, 'pages/catering.html', {'form': form, 'packages': packages})
    else:
        form = CateringOrderForm()
    
    return render(request, 'pages/catering.html', {'form': form, 'packages': packages})


def catering_confirmation(request, pk):
    """Catering order confirmation page with payment option"""
    order = get_object_or_404(CateringOrder, pk=pk)
    return render(request, 'pages/catering_confirmation.html', {'order': order})


def contact(request):
    """Contact page view with contact form"""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            message = form.save()
            
            # Send SMS acknowledgment in background thread (non-blocking)
            # This prevents worker timeout from SMS hanging
            thread = threading.Thread(target=send_contact_response_sms, args=(message,), daemon=True)
            thread.start()
            
            # Send email confirmations
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


# ============ MANUAL PAYMENT VIEWS ============

def manual_service_payment(request, service_type, pk):
    """
    Display manual payment instructions for service (restaurant/conference/catering)
    Customer pays manually via M-Pesa to the provided paybill number
    """
    from django.conf import settings
    
    # Get the service object based on type
    if service_type == 'restaurant':
        service = get_object_or_404(RestaurantReservation, pk=pk)
        service_name = "Restaurant Reservation"
        reference_field = 'booking_reference'
    elif service_type == 'conference':
        service = get_object_or_404(ConferenceBooking, pk=pk)
        service_name = "Conference Booking"
        reference_field = 'booking_reference'
    elif service_type == 'catering':
        service = get_object_or_404(CateringOrder, pk=pk)
        service_name = "Catering Order"
        reference_field = 'booking_reference'
    else:
        return render(request, '404.html', status=404)
    
    reference = getattr(service, reference_field, '')
    
    context = {
        'service': service,
        'service_type': service_type,
        'service_name': service_name,
        'paybill_number': settings.HOTEL_PAYBILL_NUMBER,
        'account_number': settings.HOTEL_ACCOUNT_NUMBER,  # Use actual hotel account number
        'account_name': settings.HOTEL_ACCOUNT_NAME,
        'payment_instruction': settings.PAYMENT_INSTRUCTION_TEXT,
    }
    
    return render(request, 'pages/manual_service_payment.html', context)
