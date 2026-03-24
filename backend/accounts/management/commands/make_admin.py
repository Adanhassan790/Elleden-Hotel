from django.core.management.base import BaseCommand
from accounts.models import User


class Command(BaseCommand):
    help = 'Grant admin permissions to a user by email'

    def add_arguments(self, parser):
        parser.add_argument('email', type=str, help='User email to grant admin permissions')

    def handle(self, *args, **options):
        email = options['email']
        try:
            user = User.objects.get(email=email)
            user.is_staff = True
            user.is_superuser = True
            user.user_type = 'admin'
            user.save()
            self.stdout.write(self.style.SUCCESS(f'✓ {email} is now an admin!'))
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f'✗ User with email {email} not found'))
