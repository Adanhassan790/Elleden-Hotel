"""
WSGI config for Elleden Hotel project.
"""
import os
import sys
from pathlib import Path
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elleden.settings')

# Initialize Django first
application = get_wsgi_application()

# Now we can access Django settings
# Get the static files root from Django settings
static_root = str(settings.STATIC_ROOT)

# Wrap with WhiteNoise to serve static files
application = WhiteNoise(
    application,
    root=static_root,
    max_age=31536000,  # 1 year
    mimetypes={'woff': 'font/woff', 'woff2': 'font/woff2'},
)


