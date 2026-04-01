"""
Management command to create a test payment for a booking
Usage: python manage.py create_test_payment --booking EH26040131CC --amount 4500 --method cash
"""
from django.core.management.base import BaseCommand
from bookings.models import Booking, Payment
from accounts.models import User
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Create a test payment for a booking to trigger SMS confirmations'
    
    def add_arguments(self, parser):
        parser.add_argument('--booking', type=str, help='Booking reference (e.g., EH26040131CC)', required=True)
        parser.add_argument('--amount', type=float, help='Payment amount (e.g., 4500)', required=True)
        parser.add_argument('--method', type=str, default='cash', 
                          choices=['cash', 'mpesa', 'card', 'bank_transfer', 'other'],
                          help='Payment method')
        parser.add_argument('--reference', type=str, default='', help='Transaction reference')
    
    def handle(self, *args, **options):
        booking_ref = options['booking']
        amount = options['amount']
        method = options['method']
        reference = options['reference'] or f'TEST-{booking_ref}'
        
        try:
            booking = Booking.objects.get(booking_reference=booking_ref)
        except Booking.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'❌ Booking {booking_ref} not found'))
            return
        
        try:
            # Get admin user for received_by field
            admin_user = User.objects.filter(is_staff=True).first()
            if not admin_user:
                self.stdout.write(self.style.ERROR('❌ No admin user found'))
                return
            
            # Create payment
            payment = Payment.objects.create(
                booking=booking,
                amount=amount,
                payment_method=method,
                transaction_reference=reference,
                received_by=admin_user,
                notes=f'Test payment created via management command'
            )
            
            self.stdout.write(self.style.SUCCESS('✅ Payment Created Successfully!'))
            self.stdout.write(f'   Booking: {booking_ref}')
            self.stdout.write(f'   Amount: KES {amount:,.0f}')
            self.stdout.write(f'   Method: {method.upper()}')
            self.stdout.write(f'   Reference: {reference}')
            self.stdout.write(f'   Payment ID: {payment.id}')
            self.stdout.write('\n📱 SMS confirmation should have been sent to: {}'.format(booking.guest_phone))
            self.stdout.write('Check logs for SMS status\n')
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'❌ Error creating payment: {e}'))
