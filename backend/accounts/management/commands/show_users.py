"""
Diagnostic command to inspect the admin users in the database
Shows exactly what users exist and their permissions
"""
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()


class Command(BaseCommand):
    help = 'Show all users and their admin status'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== ALL USERS IN DATABASE ===\n'))
        
        all_users = User.objects.all().order_by('email')
        
        if not all_users.exists():
            self.stdout.write(self.style.ERROR('❌ NO USERS FOUND IN DATABASE!'))
            return
        
        for user in all_users:
            status_parts = []
            if user.is_active:
                status_parts.append('✓ ACTIVE')
            else:
                status_parts.append('✗ INACTIVE')
            
            if user.is_superuser:
                status_parts.append('👑 SUPERUSER')
            if user.is_staff:
                status_parts.append('👤 STAFF')
            if not user.is_staff and not user.is_superuser:
                status_parts.append('👥 CUSTOMER')
            
            status = ' | '.join(status_parts)
            self.stdout.write(f"📧 {user.email:30} | {status}")
        
        # Count stats
        total = all_users.count()
        admins = all_users.filter(is_superuser=True).count()
        staff = all_users.filter(is_staff=True).count()
        active = all_users.filter(is_active=True).count()
        
        self.stdout.write('\n' + self.style.WARNING('=== SUMMARY ==='))
        self.stdout.write(f'Total users: {total}')
        self.stdout.write(f'Superusers: {admins}')
        self.stdout.write(f'Staff: {staff}')
        self.stdout.write(f'Active: {active}')
        
        if admins == 0:
            self.stdout.write(self.style.ERROR('\n❌ WARNING: NO ADMIN USERS FOUND!'))
            self.stdout.write('Run: python manage.py create_admin_user youremail@example.com')
