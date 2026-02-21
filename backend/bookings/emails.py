from django.core.mail import send_mail, EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings


def send_booking_confirmation_email(booking):
    """Send booking confirmation email to guest"""
    subject = f'Booking Confirmation - {booking.booking_reference} | Elleden Hotel'
    
    context = {
        'booking': booking,
        'hotel_name': 'Elleden Hotel',
        'hotel_phone': '+254 759 435 880',
        'hotel_email': 'elledenhotelltd@gmail.com',
        'hotel_address': 'Marsabit Moyale Highway, Elleden Plaza, Marsabit, Kenya',
    }
    
    html_content = render_to_string('emails/booking_confirmation.html', context)
    text_content = strip_tags(html_content)
    
    try:
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[booking.guest_email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def send_booking_status_update_email(booking, old_status):
    """Send email when booking status changes"""
    subject = f'Booking Update - {booking.booking_reference} | Elleden Hotel'
    
    status_messages = {
        'confirmed': 'Your booking has been confirmed!',
        'cancelled': 'Your booking has been cancelled.',
        'checked_in': 'Welcome! You have checked in successfully.',
        'checked_out': 'Thank you for staying with us!',
    }
    
    context = {
        'booking': booking,
        'status_message': status_messages.get(booking.status, f'Your booking status is now: {booking.status}'),
        'hotel_name': 'Elleden Hotel',
        'hotel_phone': '+254 759 435 880',
        'hotel_email': 'elledenhotelltd@gmail.com',
    }
    
    html_content = render_to_string('emails/booking_status_update.html', context)
    text_content = strip_tags(html_content)
    
    try:
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[booking.guest_email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False


def send_payment_receipt_email(payment):
    """Send payment receipt email"""
    booking = payment.booking
    subject = f'Payment Receipt - {booking.booking_reference} | Elleden Hotel'
    
    context = {
        'payment': payment,
        'booking': booking,
        'hotel_name': 'Elleden Hotel',
        'hotel_phone': '+254 759 435 880',
        'hotel_email': 'elledenhotelltd@gmail.com',
    }
    
    html_content = render_to_string('emails/payment_receipt.html', context)
    text_content = strip_tags(html_content)
    
    try:
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[booking.guest_email]
        )
        email.attach_alternative(html_content, "text/html")
        email.send()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False
