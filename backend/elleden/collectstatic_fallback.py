#!/usr/bin/env python
"""
Fallback script to ensure static files are available.
Runs collectstatic, and if files aren't found afterward, copies manually.
"""
import os
import sys
import shutil
from pathlib import Path

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elleden.settings')
import django
django.setup()

from django.conf import settings

print("=" * 60)
print("COLLECTSTATIC FALLBACK SCRIPT")
print("=" * 60)

static_root = Path(settings.STATIC_ROOT)
source_dir = Path(settings.STATICFILES_DIRS[0]) if settings.STATICFILES_DIRS else None

print(f"\nSource: {source_dir}")
print(f"Destination: {static_root}")

# Ensure destination exists
static_root.mkdir(parents=True, exist_ok=True)

# Try collectstatic first
print("\n1. Attempting collectstatic...")
try:
    from django.core.management import call_command
    call_command('collectstatic', '--noinput', '--clear', verbosity=2, interactive=False)
    print("✓ collectstatic completed")
except Exception as e:
    print(f"✗ collectstatic error (will try copy): {e}")

# Check if files exist
if source_dir and source_dir.exists():
    css_in_static = list(source_dir.glob('css/*.css'))
    css_in_collected = list(static_root.glob('css/*.css'))
    
    print(f"\n2. Checking files:")
    print(f"   Source static/css: {len(css_in_static)} files")
    print(f"   Collected staticfiles/css: {len(css_in_collected)} files")
    
    # If not collected, copy manually
    if not css_in_collected and css_in_static:
        print(f"\n3. No CSS in staticfiles, copying manually from {source_dir}...")
        try:
            for item in source_dir.iterdir():
                if item.is_dir():
                    dest = static_root / item.name
                    # Remove if exists
                    if dest.exists():
                        shutil.rmtree(dest, ignore_errors=True)
                    # Copy directory
                    shutil.copytree(item, dest)
                    count = len(list(dest.glob('*')))
                    print(f"   ✓ Copied {item.name}/ ({count} files)")
                else:
                    shutil.copy2(item, static_root / item.name)
                    print(f"   ✓ Copied {item.name}")
            
            # Verify
            css_after = list(static_root.glob('css/*.css'))
            js_after = list(static_root.glob('js/*.js'))
            images_after = list(static_root.glob('images/*'))
            print(f"\n   After copy - CSS: {len(css_after)}, JS: {len(js_after)}, Images: {len(images_after)}")
        except Exception as e:
            print(f"   ✗ Copy failed: {e}")
            sys.exit(1)
    else:
        print(f"\n3. Files already collected ✓")
else:
    print(f"\n✗ ERROR: Source directory not found: {source_dir}")
    sys.exit(1)

print("\n" + "=" * 60)
print("COLLECTSTATIC COMPLETED")
print("=" * 60)

