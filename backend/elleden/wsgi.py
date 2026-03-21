"""
WSGI config for Elleden Hotel project.
"""
import os
import sys
import logging
from pathlib import Path
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elleden.settings')

# Initialize Django first
application = get_wsgi_application()

# Configure logging
logger = logging.getLogger(__name__)

# Get the static files root from Django settings
static_root = str(settings.STATIC_ROOT)

# In production, wrap with WhiteNoise for static file serving
# WhiteNoise allows serving static files efficiently without relying on Django
try:
    application = WhiteNoise(
        application,
        root=static_root,
        max_age=31536000,  # 1 year
        mimetypes={'woff': 'font/woff', 'woff2': 'font/woff2'},
        index_file=False,  # Don't try to serve index.html for directories
    )
    logger.info(f"WhiteNoise initialized with static root: {static_root}")
except Exception as e:
    logger.error(f"WhiteNoise initialization failed: {e}")  
    # If WhiteNoise fails, application will still work but static files won't be served efficiently




