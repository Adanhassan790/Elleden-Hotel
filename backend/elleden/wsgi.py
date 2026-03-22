"""
WSGI config for Elleden Hotel project.
Handles both dynamic content and static file serving.
"""
import os
import sys
import logging
import shutil
from pathlib import Path
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elleden.settings')

# Initialize Django application
application = get_wsgi_application()

# Configure logging
logger = logging.getLogger(__name__)

# CRITICAL: Ensure migrations are run on startup
# This is essential for production where migrations might not have run
try:
    from django.core.management import call_command
    from django.db import connection
    
    # Check if we can connect to database and if migrations have been applied
    try:
        with connection.cursor() as cursor:
            # Try to query a table that should exist if migrations ran
            cursor.execute("SELECT 1 FROM pages_cateringpackage LIMIT 1;")
    except Exception as e:
        # Table doesn't exist, run migrations
        logger.warning(f"⚠ Migration tables missing! Running migrations now...")
        try:
            call_command('migrate', verbosity=1)
            logger.info("✅ Migrations completed successfully")
        except Exception as migrate_error:
            logger.error(f"❌ Failed to run migrations: {migrate_error}")
            
except Exception as e:
    logger.warning(f"⚠ Migration check failed: {e}")

# CRITICAL: Copy static files on every startup to ensure they exist
# This is crucial for production where staticfiles/ might be empty
try:
    from django.conf import settings
    
    src = Path(settings.BASE_DIR) / 'static'
    dst = Path(settings.STATIC_ROOT)
    
    if src.exists() and not (dst / 'css' / 'style.css').exists():
        logger.warning(f"⚠ staticfiles/css/style.css missing! Copying from source...")
        dst.mkdir(parents=True, exist_ok=True)
        
        copied_count = 0
        for src_file in src.rglob('*'):
            if src_file.is_file():
                rel_path = src_file.relative_to(src)
                dst_file = dst / rel_path
                dst_file.parent.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src_file, dst_file)
                copied_count += 1
        
        logger.info(f"✅ Copied {copied_count} static files to {dst}")
    else:
        logger.info(f"✓ Static files already present in {dst}")
        
except Exception as e:
    logger.error(f"❌ Error ensuring static files: {e}")
    import traceback
    traceback.print_exc()

# WhiteNoise is optional - use it for efficiency if files exist
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




