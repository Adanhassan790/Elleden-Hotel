from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    verbose_name = 'User Accounts'
    
    def ready(self):
        """Run startup tasks when the app initializes"""
        if hasattr(self, '_ensured_admin'):
            return
        self._ensured_admin = True
        self.ensure_admin_user()
    
    def ensure_admin_user(self):
        """
        Ensure admin@elleden.com user exists in production.
        Mirrors the development admin user with the same password hash.
        """
        try:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            
            email = 'admin@elleden.com'
            password_hash = 'pbkdf2_sha256$600000$BoXhsVE3xJvuvDY4IwHASO$cZfMg467+4xxrSDs68m5Qq+X+JOf1qRZNdU97Z4tQzk='
            
            # Check if user already exists
            if not User.objects.filter(email=email).exists():
                User.objects.create(
                    email=email,
                    first_name='Admin',
                    last_name='User',
                    is_staff=True,
                    is_superuser=True,
                    is_active=True,
                    user_type='admin',
                    password=password_hash
                )
                print(f"✓ Created admin user: {email}")
            else:
                print(f"✓ Admin user already exists: {email}")
        
        except Exception as e:
            # Log but don't crash - app should still work
            import traceback
            print(f"⚠ Error ensuring admin user: {str(e)}")
            traceback.print_exc()
