"""
Management command to list and manage admin users
Useful for production debugging
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'List all admin and staff users in the database'

    def add_arguments(self, parser):
        parser.add_argument(
            '--create-admin',
            type=str,
            help='Create new admin user: --create-admin email@example.com'
        )
        parser.add_argument(
            '--set-password',
            type=str,
            help='Set password for admin user: --set-password email@example.com newpassword'
        )

    def handle(self, *args, **options):
        if options['create_admin']:
            self.create_admin(options['create_admin'])
        elif options['set_password']:
            email_and_pass = options['set_password'].split(' ', 1)
            if len(email_and_pass) != 2:
                self.stdout.write(self.style.ERROR('Format: --set-password email@example.com newpassword'))
                return
            email, password = email_and_pass
            self.set_password(email, password)
        else:
            self.list_admins()

    def list_admins(self):
        """List all admin and staff users"""
        self.stdout.write(self.style.SUCCESS('=== Admin & Staff Users ===\n'))
        
        admins = User.objects.filter(is_staff=True).order_by('email')
        
        if not admins.exists():
            self.stdout.write(self.style.WARNING('No admin users found!'))
            return
        
        for user in admins:
            status = '👑 SUPERUSER' if user.is_superuser else '👤 STAFF'
            active = '✓ ACTIVE' if user.is_active else '✗ INACTIVE'
            self.stdout.write(
                f"{status:15} | {user.email:30} | {active:10} | "
                f"{user.first_name} {user.last_name}".strip()
            )
    
    def create_admin(self, email):
        """Create a new admin user"""
        if User.objects.filter(email=email).exists():
            self.stdout.write(self.style.ERROR(f'User {email} already exists!'))
            return
        
        # Generate a random password
        import secrets
        password = secrets.token_urlsafe(12)
        
        user = User.objects.create_superuser(
            email=email,
            password=password,
            first_name='Admin',
            last_name='User'
        )
        
        self.stdout.write(self.style.SUCCESS(f'✓ Created superuser: {email}'))
        self.stdout.write(f'Password: {password}')
        self.stdout.write(self.style.WARNING('⚠ Save this password securely!'))

    def set_password(self, email, password):
        """Set password for an admin user"""
        try:
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f'✓ Password updated for {email}'))
            self.stdout.write(f'New password: {password}')
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'User {email} not found!'))
