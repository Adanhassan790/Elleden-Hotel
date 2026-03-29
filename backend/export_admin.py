#!/usr/bin/env python
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elleden.settings')
django.setup()

from accounts.models import User

try:
    user = User.objects.get(email='admin@elleden.com')
    print(f'✓ Found admin user: {user.email}')
    print(f'  First Name: {user.first_name}')
    print(f'  Last Name: {user.last_name}')
    print(f'  is_staff: {user.is_staff}')
    print(f'  is_superuser: {user.is_superuser}')
    print(f'  Password Hash: {user.password}')
except User.DoesNotExist:
    print('✗ admin@elleden.com not found in local database')
    # List all users
    print('\nAll users in local database:')
    for u in User.objects.all():
        print(f'  - {u.email} (is_superuser: {u.is_superuser})')
except Exception as e:
    print(f'Error: {e}')
