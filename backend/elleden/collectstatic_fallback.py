#!/usr/bin/env python
"""
Fallback script to ensure static files are collected.
Runs collectstatic, and if files aren't found afterward, copies manually.
"""
import os
import sys
import shutil
from pathlib import Path
from django.core.management import execute_from_command_line

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'elleden.settings')
import django
django.setup()

from django.conf import settings

print("=" * 60)
print("COLLECTSTATIC FALLBACK SCRIPT")
print("=" * 60)

# Try collectstatic
print("\n1. Running python manage.py collectstatic...")
try:
    execute_from_command_line(['manage.py', 'collectstatic', '--noinput', '--clear', '--verbosity', '2'])
    print("✓ collectstatic completed")
except Exception as e:
    print(f"✗ collectstatic failed: {e}")

# Check if files were collected
static_root = Path(settings.STATIC_ROOT)
css_files = list(static_root.glob('css/*.css'))
js_files = list(static_root.glob('js/*.js'))

print(f"\n2. Checking collected files:")
print(f"   CSS files in staticfiles/: {len(css_files)}")
print(f"   JS files in staticfiles/: {len(js_files)}")

# If no files, copy manually
if not css_files and not js_files:
    print("\n3. No files found in staticfiles/, copying manually...")
    source = Path(settings.STATICFILES_DIRS[0])
    
    if source.exists():
        print(f"   Copying from {source} to {static_root}")
        for item in source.iterdir():
            if item.is_dir():
                dest = static_root / item.name
                if dest.exists():
                    shutil.rmtree(dest)
                shutil.copytree(item, dest)
                print(f"   ✓ Copied {item.name}/")
            else:
                shutil.copy2(item, static_root / item.name)
                print(f"   ✓ Copied {item.name}")
        
        # Verify
        css_files = list(static_root.glob('css/*.css'))
        js_files = list(static_root.glob('js/*.js'))
        print(f"\n   After manual copy - CSS: {len(css_files)}, JS: {len(js_files)}")
    else:
        print(f"   ✗ Source directory not found: {source}")
        sys.exit(1)
else:
    print("\n3. Files already collected, no manual copy needed ✓")

print("\n" + "=" * 60)
print("COLLECTSTATIC FALLBACK COMPLETE")
print("=" * 60)
