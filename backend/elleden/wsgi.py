"""
WSGI config for Elleden Hotel project.
Handles both dynamic content and static file serving via WhiteNoise.
"""
import os
import sys
import logging
from pathlib import Path
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elleden.settings')

# Initialize Django application
application = get_wsgi_application()

# Configure logging for debugging static file issues
logger = logging.getLogger(__name__)

# Get static root path from Django settings  
static_root = str(settings.STATIC_ROOT)

# Verify the path exists before wrapping with WhiteNoise
try:
    static_path = Path(static_root)
    if not static_path.exists():
        logger.warning(f"Static root does not exist: {static_root}")
        # Create it if possible
        try:
            static_path.mkdir(parents=True, exist_ok=True)
            logger.info(f"Created static root directory: {static_root}")
        except Exception as mkdir_err:
            logger.error(f"Failed to create static root: {mkdir_err}")
except Exception as e:
    logger.error(f"Error checking static path: {e}")

# Wrap Django application with WhiteNoise for efficient static file serving
try:
    application = WhiteNoise(
        application,
        root=static_root,
        max_age=31536000,  # 1 year for browser caching
        mimetypes={
            'woff': 'font/woff',
            'woff2': 'font/woff2',
            'css': 'text/css',
            'js': 'application/javascript',
        },
        index_file=False,  # Don't serve index.html for directories
        add_headers_function=lambda environ, headers: headers.update({
            'Access-Control-Allow-Origin': '*'  # Allow cross-origin if needed
        })
    )
    logger.info(f"✓ WhiteNoise initialized successfully with root: {static_root}")
    
    # Log the static directory contents for debugging
    static_css_count = len(list(Path(static_root).glob('css/*.css')))
    static_js_count = len(list(Path(static_root).glob('js/*.js')))
    logger.info(f"  └─ Found {static_css_count} CSS files and {static_js_count} JS files")
    
except Exception as e:
    logger.error(f"✗ WhiteNoise initialization failed: {e}")
    logger.error("Static files will not be served efficiently. Using Django fallback.")
    # Continue anyway - Django URL handlers will serve as fallback




