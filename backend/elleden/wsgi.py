"""
WSGI config for Elleden Hotel project.
"""
import os
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elleden.settings')
application = get_wsgi_application()

# Wrap with WhiteNoise to serve static files efficiently
application = WhiteNoise(
    application,
    root=os.path.join(os.path.dirname(__file__), '..', 'staticfiles'),
    max_age=31536000,  # 1 year
    immutable_file_test=lambda path, url: '.css' in url or '.js' in url or '.woff' in url
)

