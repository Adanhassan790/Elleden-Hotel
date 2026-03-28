"""
Quick fix to make a user a superuser/admin
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Make a user a superuser/admin'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='User email')

    def handle(self, *args, **options):
        email = options['email']
        
        try:
            user = User.objects.get(email=email)
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.save()
            self.stdout.write(self.style.SUCCESS(f'✓ {email} is now a superuser!'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'✗ User {email} not found!'))
