"""
SMS Service Module for Elleden Hotel
Uses Africa's Talking SMS Gateway - Popular in Kenya
"""
import africastalking
from django.conf import settings
import logging

logger = logging.getLogger(__name__)


class SMSService:
    """SMS Service using Africa's Talking"""
    
    def __init__(self):
        # Initialize Africa's Talking
        self.username = getattr(settings, 'AFRICASTALKING_USERNAME', 'sandbox')
        self.api_key = getattr(settings, 'AFRICASTALKING_API_KEY', '')
        self.sender_id = getattr(settings, 'AFRICASTALKING_SENDER_ID', None)  # Optional shortcode
        
        if self.api_key:
            africastalking.initialize(self.username, self.api_key)
            self.sms = africastalking.SMS
        else:
            self.sms = None
            logger.warning("Africa's Talking API key not configured")
    
    def format_phone(self, phone):
        """Format phone number to international format (+254...)"""
        if not phone:
            return None
        
        # Remove spaces and dashes
        phone = phone.replace(' ', '').replace('-', '')
        
        # Handle various formats
        if phone.startswith('+'):
            return phone
        elif phone.startswith('254'):
            return f'+{phone}'
        elif phone.startswith('0'):
            return f'+254{phone[1:]}'
        elif phone.startswith('7') or phone.startswith('1'):
            return f'+254{phone}'
        
        return phone
    
    def send_sms(self, phone, message):
        """Send SMS to a single recipient"""
        if not self.sms:
            logger.warning("SMS service not configured - message not sent")
            return False
        
        formatted_phone = self.format_phone(phone)
        if not formatted_phone:
            logger.error(f"Invalid phone number: {phone}")
            return False
        
        try:
            kwargs = {
                'message': message,
                'recipients': [formatted_phone]
            }
            if self.sender_id:
                kwargs['sender_id'] = self.sender_id
            
            response = self.sms.send(**kwargs)
            logger.info(f"SMS sent to {formatted_phone}: {response}")
            return True
        except Exception as e:
            logger.error(f"Failed to send SMS to {formatted_phone}: {str(e)}")
            return False
    
    def send_bulk_sms(self, recipients, message):
        """Send SMS to multiple recipients"""
        if not self.sms:
            logger.warning("SMS service not configured")
            return False
        
        formatted_phones = [self.format_phone(p) for p in recipients if self.format_phone(p)]
        if not formatted_phones:
            return False
        
        try:
            kwargs = {
                'message': message,
                'recipients': formatted_phones
            }
            if self.sender_id:
                kwargs['sender_id'] = self.sender_id
            
            response = self.sms.send(**kwargs)
            logger.info(f"Bulk SMS sent: {response}")
            return True
        except Exception as e:
            logger.error(f"Failed to send bulk SMS: {str(e)}")
            return False


# Pre-built SMS templates
class SMSTemplates:
    """SMS message templates for Elleden Hotel"""
    
    @staticmethod
    def room_booking_confirmation(booking):
        """Room booking confirmation SMS"""
        return (
            f"Elleden Hotel: Booking Confirmed!\n"
            f"Ref: {booking.booking_reference}\n"
            f"Room: {booking.room_type.name}\n"
            f"Check-in: {booking.check_in_date.strftime('%b %d, %Y')}\n"
            f"Check-out: {booking.check_out_date.strftime('%b %d, %Y')}\n"
            f"Total: KES {booking.total_amount:,.0f}\n"
            f"Call: +254759435880"
        )
    
    @staticmethod
    def room_booking_status_update(booking):
        """Room booking status update SMS"""
        return (
            f"Elleden Hotel: Booking Update\n"
            f"Ref: {booking.booking_reference}\n"
            f"Status: {booking.get_status_display()}\n"
            f"For queries: +254759435880"
        )
    
    @staticmethod
    def restaurant_reservation_confirmation(reservation):
        """Restaurant reservation SMS"""
        return (
            f"Elleden Hotel Restaurant\n"
            f"Reservation Confirmed!\n"
            f"Ref: {reservation.booking_reference}\n"
            f"Date: {reservation.date.strftime('%b %d, %Y')}\n"
            f"Time: {reservation.time.strftime('%I:%M %p')}\n"
            f"Guests: {reservation.guests}\n"
            f"See you soon!"
        )
    
    @staticmethod
    def conference_booking_confirmation(booking):
        """Conference booking SMS"""
        return (
            f"Elleden Hotel Conference\n"
            f"Booking Confirmed!\n"
            f"Ref: {booking.booking_reference}\n"
            f"Date: {booking.event_date.strftime('%b %d, %Y')}\n"
            f"Attendees: {booking.attendees}\n"
            f"Total: KES {booking.total_amount:,.0f}\n"
            f"Call: +254759435880"
        )
    
    @staticmethod
    def catering_order_confirmation(order):
        """Catering order SMS"""
        return (
            f"Elleden Hotel Catering\n"
            f"Order Confirmed!\n"
            f"Ref: {order.booking_reference}\n"
            f"Package: {order.package.name}\n"
            f"Date: {order.event_date.strftime('%b %d, %Y')}\n"
            f"Guests: {order.guest_count}\n"
            f"Total: KES {order.total_amount:,.0f}\n"
            f"Call: +254759435880"
        )
    
    @staticmethod
    def payment_confirmation(service_type, reference, amount):
        """Payment confirmation SMS"""
        return (
            f"Elleden Hotel Payment Received\n"
            f"Amount: KES {amount:,.0f}\n"
            f"Ref: {reference}\n"
            f"Service: {service_type}\n"
            f"Thank you!"
        )
    
    @staticmethod
    def booking_reminder(booking, hours_before=24):
        """Booking reminder SMS"""
        return (
            f"Elleden Hotel Reminder\n"
            f"Your check-in is tomorrow!\n"
            f"Ref: {booking.booking_reference}\n"
            f"Room: {booking.room_type.name}\n"
            f"Check-in from 2:00 PM\n"
            f"See you soon!"
        )


# Convenience function
def send_sms(phone, message):
    """Quick function to send SMS"""
    service = SMSService()
    return service.send_sms(phone, message)
