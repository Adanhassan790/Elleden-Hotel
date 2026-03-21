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

from rooms.models import RoomType
from .forms import (ContactForm, RestaurantReservationForm, ConferenceBookingForm, 
                   CateringInquiryForm, CateringOrderForm)
from .models import (RestaurantReservation, ConferenceBooking, CateringOrder, 
                    CateringPackage, ServiceMpesaTransaction, ServicePayment)
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
            reservation = form.save()
            
            # Send SMS confirmation (primary notification)
            send_restaurant_reservation_sms(reservation)
            
            # Send email as backup
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
            
            return redirect('pages:restaurant_confirmation', pk=reservation.pk)
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
            booking = form.save()
            
            # Send SMS confirmation (primary notification)
            send_conference_booking_sms(booking)
            
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
            
            return redirect('pages:conference_confirmation', pk=booking.pk)
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
            order = form.save()
            
            # Send SMS confirmation (primary notification)
            send_catering_order_sms(order)
            
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
            
            return redirect('pages:catering_confirmation', pk=order.pk)
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
            
            # Send SMS acknowledgment (if phone provided)
            send_contact_response_sms(message)
            
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


# =====================
# M-Pesa Payment Views for Services
# =====================

def initiate_service_payment(request, service_type, pk):
    """Initiate M-Pesa STK Push for conference or catering payment"""
    from bookings.mpesa import MpesaClient
    
    # Get the booking/order based on service type
    if service_type == 'conference':
        booking = get_object_or_404(ConferenceBooking, pk=pk)
        amount = booking.balance_due
        phone = booking.phone
        reference = booking.booking_reference
        description = f"Conference Booking {reference}"
    elif service_type == 'catering':
        booking = get_object_or_404(CateringOrder, pk=pk)
        amount = booking.balance_due
        phone = booking.phone
        reference = booking.booking_reference
        description = f"Catering Order {reference}"
    else:
        messages.error(request, 'Invalid service type')
        return redirect('pages:home')
    
    if amount <= 0:
        messages.info(request, 'This booking is already fully paid')
        return redirect(f'pages:{service_type}_confirmation', pk=pk)
    
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number', phone)
        
        # Clean phone number
        phone_number = phone_number.replace(' ', '').replace('-', '')
        if phone_number.startswith('0'):
            phone_number = '254' + phone_number[1:]
        elif phone_number.startswith('+'):
            phone_number = phone_number[1:]
        
        # Initialize M-Pesa client and send STK Push
        mpesa = MpesaClient()
        
        try:
            response = mpesa.stk_push(
                phone_number=phone_number,
                amount=int(amount),
                account_reference=reference,
                transaction_desc=description
            )
            
            if response.get('ResponseCode') == '0':
                # Create transaction record with FK
                transaction_data = {
                    'service_type': service_type,
                    'checkout_request_id': response.get('CheckoutRequestID'),
                    'merchant_request_id': response.get('MerchantRequestID'),
                    'amount': amount,
                    'phone_number': phone_number,
                    'status': 'pending'
                }
                
                if service_type == 'conference':
                    transaction_data['conference_booking'] = booking
                else:
                    transaction_data['catering_order'] = booking
                    
                transaction = ServiceMpesaTransaction.objects.create(**transaction_data)
                
                # Update booking payment status
                booking.payment_status = 'processing'
                booking.save()
                
                return redirect('pages:service_payment_status', 
                               service_type=service_type, 
                               pk=pk,
                               transaction_id=transaction.id)
            else:
                error_msg = response.get('errorMessage', response.get('ResponseDescription', 'Unknown error'))
                messages.error(request, f'Payment initiation failed: {error_msg}')
                
        except Exception as e:
            logger.error(f"M-Pesa STK Push error: {str(e)}")
            messages.error(request, f'Payment error: {str(e)}')
    
    context = {
        'service_type': service_type,
        'booking': booking,
        'amount': amount,
    }
    return render(request, 'pages/service_payment_form.html', context)


def service_payment_status(request, service_type, pk, transaction_id):
    """Display payment status page for service payments"""
    transaction = get_object_or_404(ServiceMpesaTransaction, id=transaction_id)
    
    if service_type == 'conference':
        booking = get_object_or_404(ConferenceBooking, pk=pk)
    elif service_type == 'catering':
        booking = get_object_or_404(CateringOrder, pk=pk)
    else:
        return redirect('pages:home')
    
    context = {
        'service_type': service_type,
        'booking': booking,
        'transaction': transaction,
    }
    return render(request, 'pages/service_payment_status.html', context)


def check_service_payment_status(request, transaction_id):
    """AJAX endpoint to check M-Pesa payment status"""
    from bookings.mpesa import MpesaClient
    
    transaction = get_object_or_404(ServiceMpesaTransaction, id=transaction_id)
    
    # If already completed, return immediately
    if transaction.status in ['completed', 'failed']:
        return JsonResponse({
            'status': transaction.status,
            'message': 'Payment completed' if transaction.status == 'completed' else 'Payment failed'
        })
    
    # Query M-Pesa for status
    mpesa = MpesaClient()
    
    try:
        response = mpesa.query_stk_status(transaction.checkout_request_id)
        
        result_code = response.get('ResultCode')
        
        if result_code == '0':
            # Payment successful
            transaction.status = 'completed'
            transaction.result_code = result_code
            transaction.result_description = response.get('ResultDesc', 'Success')
            transaction.save()
            
            # Update booking and create payment record
            if transaction.service_type == 'conference':
                booking = transaction.conference_booking
            else:
                booking = transaction.catering_order
            
            booking.amount_paid += transaction.amount
            
            if booking.amount_paid >= booking.total_amount:
                booking.payment_status = 'paid'
            else:
                booking.payment_status = 'partial'
            booking.save()
            
            # Create payment record
            payment_data = {
                'service_type': transaction.service_type,
                'amount': transaction.amount,
                'payment_method': 'mpesa',
                'transaction_reference': transaction.mpesa_receipt_number or transaction.checkout_request_id,
            }
            if transaction.service_type == 'conference':
                payment_data['conference_booking'] = booking
            else:
                payment_data['catering_order'] = booking
            
            ServicePayment.objects.create(**payment_data)
            
            return JsonResponse({
                'status': 'completed',
                'message': 'Payment successful!'
            })
            
        elif result_code is not None:
            # Payment failed
            transaction.status = 'failed'
            transaction.result_code = result_code
            transaction.result_description = response.get('ResultDesc', 'Failed')
            transaction.save()
            
            return JsonResponse({
                'status': 'failed',
                'message': response.get('ResultDesc', 'Payment failed')
            })
        else:
            # Still pending
            return JsonResponse({
                'status': 'pending',
                'message': 'Waiting for payment confirmation...'
            })
            
    except Exception as e:
        logger.error(f"Error checking payment status: {str(e)}")
        return JsonResponse({
            'status': 'pending',
            'message': 'Checking payment status...'
        })


@csrf_exempt
@require_POST
def service_mpesa_callback(request):
    """Handle M-Pesa callback for service payments"""
    try:
        data = json.loads(request.body)
        logger.info(f"Service M-Pesa callback received: {data}")
        
        # Extract callback data
        stk_callback = data.get('Body', {}).get('stkCallback', {})
        checkout_request_id = stk_callback.get('CheckoutRequestID')
        result_code = str(stk_callback.get('ResultCode'))
        result_desc = stk_callback.get('ResultDesc')
        
        # Find the transaction
        try:
            transaction = ServiceMpesaTransaction.objects.get(
                checkout_request_id=checkout_request_id
            )
        except ServiceMpesaTransaction.DoesNotExist:
            logger.error(f"Transaction not found: {checkout_request_id}")
            return JsonResponse({'ResultCode': 0, 'ResultDesc': 'Accepted'})
        
        # Update transaction
        transaction.result_code = int(result_code)
        transaction.result_description = result_desc
        
        if result_code == '0':
            # Payment successful - extract details
            callback_metadata = stk_callback.get('CallbackMetadata', {}).get('Item', [])
            
            for item in callback_metadata:
                name = item.get('Name')
                value = item.get('Value')
                
                if name == 'MpesaReceiptNumber':
                    transaction.mpesa_receipt_number = value
            
            # Use the model method to complete the transaction
            transaction.mark_completed(
                mpesa_receipt=transaction.mpesa_receipt_number,
                result_desc=result_desc
            )
            
        else:
            # Payment failed
            transaction.mark_failed(int(result_code), result_desc)
            
            if transaction.service_type == 'conference' and transaction.conference_booking:
                transaction.conference_booking.payment_status = 'pending'
                transaction.conference_booking.save()
            elif transaction.service_type == 'catering' and transaction.catering_order:
                transaction.catering_order.payment_status = 'pending'
                transaction.catering_order.save()
        
        return JsonResponse({'ResultCode': 0, 'ResultDesc': 'Accepted'})
        
    except Exception as e:
        logger.error(f"Service M-Pesa callback error: {str(e)}")
        return JsonResponse({'ResultCode': 0, 'ResultDesc': 'Accepted'})
