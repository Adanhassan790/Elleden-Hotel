"""
SMS Notification Service for Pages App
Handles SMS notifications for Restaurant, Conference, and Catering services
"""
from bookings.sms import SMSService, SMSTemplates
import logging

logger = logging.getLogger(__name__)


def send_restaurant_reservation_sms(reservation):
    """Send SMS confirmation for restaurant reservation"""
    if not reservation.phone:
        logger.warning(f"No phone number for restaurant reservation {reservation.booking_reference}")
        return False
    
    try:
        sms_service = SMSService()
        message = SMSTemplates.restaurant_reservation_confirmation(reservation)
        result = sms_service.send_sms(reservation.phone, message)
        if result:
            logger.info(f"SMS sent for restaurant reservation {reservation.booking_reference}")
        return result
    except Exception as e:
        logger.error(f"Failed to send restaurant SMS: {e}")
        return False


def send_conference_booking_sms(booking):
    """Send SMS confirmation for conference booking"""
    if not booking.phone:
        logger.warning(f"No phone number for conference booking {booking.booking_reference}")
        return False
    
    try:
        sms_service = SMSService()
        message = SMSTemplates.conference_booking_confirmation(booking)
        result = sms_service.send_sms(booking.phone, message)
        if result:
            logger.info(f"SMS sent for conference booking {booking.booking_reference}")
        return result
    except Exception as e:
        logger.error(f"Failed to send conference SMS: {e}")
        return False


def send_catering_order_sms(order):
    """Send SMS confirmation for catering order"""
    if not order.phone:
        logger.warning(f"No phone number for catering order {order.booking_reference}")
        return False
    
    try:
        sms_service = SMSService()
        message = SMSTemplates.catering_order_confirmation(order)
        result = sms_service.send_sms(order.phone, message)
        if result:
            logger.info(f"SMS sent for catering order {order.booking_reference}")
        return result
    except Exception as e:
        logger.error(f"Failed to send catering SMS: {e}")
        return False


def send_service_payment_sms(service_type, booking, amount):
    """Send SMS confirmation for service payment"""
    phone = getattr(booking, 'phone', None)
    reference = getattr(booking, 'booking_reference', 'N/A')
    
    if not phone:
        return False
    
    try:
        sms_service = SMSService()
        service_names = {
            'conference': 'Conference Booking',
            'catering': 'Catering Order',
            'restaurant': 'Restaurant'
        }
        message = SMSTemplates.payment_confirmation(
            service_names.get(service_type, service_type.title()),
            reference,
            amount
        )
        result = sms_service.send_sms(phone, message)
        if result:
            logger.info(f"Payment SMS sent for {service_type} {reference}")
        return result
    except Exception as e:
        logger.error(f"Failed to send payment SMS: {e}")
        return False


def send_contact_response_sms(contact_message):
    """Send SMS acknowledging contact form submission"""
    if not contact_message.phone:
        return False
    
    try:
        sms_service = SMSService()
        message = (
            f"Elleden Hotel\n"
            f"Thank you for contacting us!\n"
            f"We received your message and will respond within 24 hours.\n"
            f"Call: +254759435880"
        )
        result = sms_service.send_sms(contact_message.phone, message)
        return result
    except Exception as e:
        logger.error(f"Failed to send contact SMS: {e}")
        return False
