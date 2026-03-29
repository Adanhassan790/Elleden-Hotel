from django.core.management.base import BaseCommand
from accounts.models import User


class Command(BaseCommand):
    help = 'Migrate admin@elleden.com user from dev to production'

    def handle(self, *args, **options):
        email = 'admin@elleden.com'
        password_hash = 'pbkdf2_sha256$600000$BoXhsVE3xJvuvDY4IwHASO$cZfMg467+4xxrSDs68m5Qq+X+JOf1qRZNdU97Z4tQzk='
        
        # Check if user already exists
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            self.stdout.write(self.style.WARNING(f'✓ User already exists: {email}'))
            self.stdout.write(f'  is_staff: {user.is_staff}')
            self.stdout.write(f'  is_superuser: {user.is_superuser}')
            return
        
        # Create the user with the same password hash
        user = User.objects.create(
            email=email,
            first_name='Admin',
            last_name='User',
            is_staff=True,
            is_superuser=True,
            is_active=True,
            user_type='admin',
            password=password_hash
        )
        
        self.stdout.write(self.style.SUCCESS(f'✓ Successfully migrated admin user: {email}'))
        self.stdout.write(f'  First Name: {user.first_name}')
        self.stdout.write(f'  Last Name: {user.last_name}')
        self.stdout.write(f'  is_staff: {user.is_staff}')
        self.stdout.write(f'  is_superuser: {user.is_superuser}')
        self.stdout.write('\n✅ Admin user ready! Login with:')
        self.stdout.write(f'  Email: {email}')
        self.stdout.write(f'  Password: (your dev password)')
