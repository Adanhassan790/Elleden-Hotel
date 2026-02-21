"""
ASGI config for Elleden Hotel project.
"""
import os
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elleden.settings')
application = get_asgi_application()
