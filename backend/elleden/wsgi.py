"""
WSGI config for Elleden Hotel project.
"""
import os
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elleden.settings')
application = get_wsgi_application()
