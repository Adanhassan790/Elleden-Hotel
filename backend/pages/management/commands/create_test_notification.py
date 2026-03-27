from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from pages.models import Notification

User = get_user_model()


class Command(BaseCommand):
    help = 'Create a test notification for the first admin user'

    def handle(self, *args, **options):
        # Get the first admin user
        admin_user = User.objects.filter(is_staff=True).first()
        
        if not admin_user:
            self.stdout.write(self.style.ERROR('No admin user found. Please create one first.'))
            return
        
        # Create test notifications
        notifications = [
            {
                'title': 'Welcome to Notifications!',
                'message': 'This is your first notification. You can view all notifications on this page.',
                'notification_type': 'system',
                'icon': 'fa-smile',
            },
            {
                'title': 'Booking Update',
                'message': 'Your recent booking has been confirmed and is awaiting payment.',
                'notification_type': 'booking',
                'icon': 'fa-calendar-check',
            },
            {
                'title': 'Payment Notification',
                'message': 'Payment received for your booking. Thank you!',
                'notification_type': 'payment',
                'icon': 'fa-credit-card',
            }
        ]
        
        for notif_data in notifications:
            Notification.objects.create(
                user=admin_user,
                title=notif_data['title'],
                message=notif_data['message'],
                notification_type=notif_data['notification_type'],
                icon=notif_data['icon'],
            )
            self.stdout.write(self.style.SUCCESS(f"Created notification: {notif_data['title']}"))
        
        self.stdout.write(self.style.SUCCESS(f'\nSuccessfully created {len(notifications)} test notifications for {admin_user.email}'))
