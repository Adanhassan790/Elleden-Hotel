"""
Command to create or reset an admin user directly
This creates a new superuser or resets existing user to be superuser
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
import secrets

User = get_user_model()


class Command(BaseCommand):
    help = 'Create a new admin user or upgrade existing to admin'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='Admin email')
        parser.add_argument('--password', type=str, default=None, help='Set specific password')

    def handle(self, *args, **options):
        email = options['email']
        password = options['password'] or secrets.token_urlsafe(12)
        
        # Check if user exists
        user, created = User.objects.get_or_create(
            email=email,
            defaults={
                'first_name': 'Admin',
                'last_name': 'User',
                'user_type': 'admin',
            }
        )
        
        # Ensure all admin flags are set
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.set_password(password)
        user.save()
        
        if created:
            self.stdout.write(self.style.SUCCESS(f'✓ CREATED new superuser: {email}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'✓ UPGRADED existing user to admin: {email}'))
        
        self.stdout.write(f'\n📧 Email: {email}')
        self.stdout.write(f'🔑 Password: {password}')
        self.stdout.write(f'🌐 Admin URL: /admin/')
        self.stdout.write(self.style.WARNING('\n⚠  Save this password securely!'))
