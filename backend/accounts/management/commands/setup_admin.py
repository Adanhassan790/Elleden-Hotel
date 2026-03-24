from django.core.management.base import BaseCommand
from django.contrib.auth.models import User as DjangoUser
from accounts.models import User
from django.contrib.auth.hashers import make_password


class Command(BaseCommand):
    help = 'Setup admin user with proper configuration'

    def handle(self, *args, **options):
        email = 'qonqona@gmail.com'
        password = 'ElledenHotel@2024'  # Set a known password
        
        try:
            user = User.objects.get(email=email)
            # Set password
            user.set_password(password)
            user.is_staff = True
            user.is_superuser = True
            user.is_active = True
            user.user_type = 'admin'
            user.save()
            self.stdout.write(self.style.SUCCESS(f'✓ Admin setup complete for {email}'))
            self.stdout.write(f'Password: {password}')
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'✗ User {email} not found'))
