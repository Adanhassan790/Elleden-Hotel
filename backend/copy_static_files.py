#!/usr/bin/env python
"""
Guaranteed static file copy script.
Ensures static files are available even if collectstatic fails.
"""
import os
import shutil
from pathlib import Path

def copy_static_files():
    """Copy files from static/ to staticfiles/ directory"""
    base_dir = Path(__file__).resolve().parent
    src = base_dir / 'static'
    dst = base_dir / 'staticfiles'
    
    # Create destination if it doesn't exist
    dst.mkdir(parents=True, exist_ok=True)
    
    if not src.exists():
        print(f"❌ Source directory not found: {src}")
        return False
    
    total_files = 0
    try:
        # Copy all files from static to staticfiles
        for src_file in src.rglob('*'):
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
        
        print(f"\n✅ Successfully copied {total_files} files to {dst}")
        
        # Verify CSS files exist
        css_files = list((dst / 'css').glob('*.css'))
        print(f"✓ Found {len(css_files)} CSS files in {dst}/css/")
        for css in css_files:
            print(f"  - {css.name}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error copying files: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    success = copy_static_files()
    exit(0 if success else 1)
