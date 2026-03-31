"""
Management command to test Africa's Talking SMS service
Usage: python manage.py test_sms [--phone PHONE_NUMBER] [--message MESSAGE]
"""
from django.core.management.base import BaseCommand
from django.conf import settings
import logging

from bookings.sms import SMSService, SMSTemplates

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = 'Test Africa\'s Talking SMS service connectivity and credentials'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--phone',
            type=str,
            help='Phone number to send test SMS to (e.g., +254759435880)',
            required=False
        )
        parser.add_argument(
            '--message',
            type=str,
            help='Custom message to send (default: test message)',
            required=False
        )
    
    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('🔍 Testing Africa\'s Talking SMS Service...'))
        self.stdout.write('-' * 60)
        
        # 1. Check environment variables
        self.stdout.write('\n📋 Checking Configuration:')
        username = settings.AFRICASTALKING_USERNAME
        api_key = settings.AFRICASTALKING_API_KEY
        sender_id = settings.AFRICASTALKING_SENDER_ID
        
        self.stdout.write(f'  Username: {username if username != "sandbox" else self.style.WARNING(username)}')
        self.stdout.write(f'  API Key: {"***" + api_key[-4:] if api_key else self.style.ERROR("NOT SET")}')
        self.stdout.write(f'  Sender ID: {sender_id if sender_id else "(not configured)"}')
        
        if username == 'sandbox':
            self.stdout.write(self.style.WARNING('  ⚠️ Using SANDBOX username (development mode)'))
        
        if not api_key:
            self.stdout.write(self.style.ERROR('\n❌ ERROR: AFRICASTALKING_API_KEY is not set!'))
            return
        
        # 2. Initialize SMS Service
        self.stdout.write('\n🔌 Initializing SMS Service...')
        try:
            sms_service = SMSService()
            if sms_service.sms:
                self.stdout.write(self.style.SUCCESS('  ✅ SMS service initialized successfully!'))
            else:
                self.stdout.write(self.style.ERROR('  ❌ SMS service failed to initialize (see logs)'))
                return
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'  ❌ Error initializing SMS: {e}'))
            return
        
        # 3. Optionally send test SMS
        phone = options.get('phone')
        message = options.get('message')
        
        if phone:
            self.stdout.write('\n📱 Sending Test SMS...')
            test_message = message or f"✅ SMS Test from Elleden Hotel Production (sent {__import__('datetime').datetime.now().strftime('%H:%M:%S')})"
            
            try:
                result = sms_service.send_sms(phone, test_message)
                if result:
                    self.stdout.write(self.style.SUCCESS(f'  ✅ SMS sent successfully to {phone}!'))
                    self.stdout.write(f'  Message: {test_message}')
                else:
                    self.stdout.write(self.style.ERROR(f'  ❌ SMS failed to send to {phone}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'  ❌ Error sending SMS: {e}'))
        else:
            self.stdout.write('\n💡 To send a test SMS, use:')
            self.stdout.write('   python manage.py test_sms --phone +254759435880')
            self.stdout.write('   python manage.py test_sms --phone +254759435880 --message "Custom message"')
        
        self.stdout.write('\n' + '=' * 60)
        self.stdout.write(self.style.SUCCESS('✅ SMS Service Test Complete!'))
        self.stdout.write('=' * 60)
