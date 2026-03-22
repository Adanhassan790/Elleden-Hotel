#!/usr/bin/env python
"""
Guaranteed static file copy script.
Ensures static files are available even if collectstatic fails.
"""
import os
import sys
import shutil
from pathlib import Path

def copy_static_files():
    """Copy files from static/ to staticfiles/ directory"""
    # Get the directory where manage.py is located (backend/)
    base_dir = Path(__file__).resolve().parent
    src = base_dir / 'static'
    dst = base_dir / 'staticfiles'
    
    print(f"DEBUG: Script location: {__file__}", file=sys.stderr)
    print(f"DEBUG: Base dir: {base_dir}", file=sys.stderr)
    print(f"DEBUG: Source: {src}", file=sys.stderr)
    print(f"DEBUG: Destination: {dst}", file=sys.stderr)
    
    # Create destination if it doesn't exist
    dst.mkdir(parents=True, exist_ok=True)
    print(f"✓ Destination directory created/exists: {dst}", file=sys.stderr)
    
    if not src.exists():
        print(f"❌ Source directory not found: {src}", file=sys.stderr)
        print(f"   Contents of base_dir ({base_dir}):", file=sys.stderr)
        for item in base_dir.iterdir():
            print(f"   - {item}", file=sys.stderr)
        return False
    
    print(f"✓ Source directory found: {src}", file=sys.stderr)
    print(f"   Contents:", file=sys.stderr)
    for item in src.iterdir():
        print(f"   - {item}", file=sys.stderr)
    
    total_files = 0
    try:
        # Copy all files from static to staticfiles
        all_files = list(src.rglob('*'))
        print(f"📊 Total items to process: {len(all_files)}", file=sys.stderr)
        
        for src_file in all_files:
            if src_file.is_file():
                # Determine relative path
                rel_path = src_file.relative_to(src)
                dst_file = dst / rel_path
                
                # Create parent directories if needed
                dst_file.parent.mkdir(parents=True, exist_ok=True)
                
                # Copy file
                shutil.copy2(src_file, dst_file)
                total_files += 1
                print(f"✓ Copied: {rel_path}")
        
        print(f"\n✅ Successfully copied {total_files} files to {dst}", file=sys.stderr)
        
        # Verify CSS files exist
        css_files = list((dst / 'css').glob('*.css')) if (dst / 'css').exists() else []
        print(f"✅ Verification: Found {len(css_files)} CSS files in {dst}/css/", file=sys.stderr)
        for css in css_files:
            print(f"  ✓ {css.name}")
        
        # List all files in staticfiles
        all_staticfiles = list(dst.rglob('*'))
        print(f"📊 Total files in staticfiles: {len([f for f in all_staticfiles if f.is_file()])}", file=sys.stderr)
        
        return True
        
    except Exception as e:
        print(f"❌ Error copying files: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        return False

if __name__ == '__main__':
    success = copy_static_files()
    exit(0 if success else 1)
