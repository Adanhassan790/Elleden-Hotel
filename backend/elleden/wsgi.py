"""
WSGI config for Elleden Hotel project.
Handles both dynamic content and static file serving.
"""
import os
import sys
import logging
from pathlib import Path
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elleden.settings')

# Initialize Django application
application = get_wsgi_application()

# Configure logging
logger = logging.getLogger(__name__)

# WhiteNoise is optional - use it if available for efficiency
# But Django's serve view is the fallback
from django.conf import settings

static_root = str(settings.STATIC_ROOT)

try:
    from whitenoise import WhiteNoise
    
    # Verify static files exist before wrapping
    static_path = Path(static_root)
    css_count = len(list(static_path.glob('css/*.css')))
    
    if css_count > 0:
        application = WhiteNoise(
            application,
            root=static_root,
            max_age=31536000,  # 1 year
            mimetypes={
                'woff': 'font/woff',
                'woff2': 'font/woff2',
                'css': 'text/css',
                'js': 'application/javascript',
            },
            index_file=False,
        )
        logger.info(f"✓ WhiteNoise initialized with {css_count} CSS files at {static_root}")
    else:
        logger.warning(f"⚠ WhiteNoise skipped - no CSS files found in {static_root}")
        logger.warning("  Django serve view will handle static files instead")
        
except ImportError:
    logger.info("WhiteNoise not available, using Django serve view for static files")
except Exception as e:
    logger.error(f"WhiteNoise initialization failed: {e}")
    logger.info("Django serve view will handle static files as fallback")




