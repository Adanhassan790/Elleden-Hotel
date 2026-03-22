"""
Django management command to copy static files.
This ensures static files are available even if collectstatic fails.
"""
import shutil
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Copy static files from source to destination'

    def handle(self, *args, **options):
        src = Path(settings.BASE_DIR) / 'static'
        dst = Path(settings.STATIC_ROOT)
        
        self.stdout.write(f"Source: {src}")
        self.stdout.write(f"Destination: {dst}")
        
        # Create destination directory
        dst.mkdir(parents=True, exist_ok=True)
        
        if not src.exists():
            self.stderr.write(f"❌ Source directory not found: {src}")
            return
        
        total_files = 0
        try:
            # Copy all files
            for src_file in src.rglob('*'):
                if src_file.is_file():
                    rel_path = src_file.relative_to(src)
                    dst_file = dst / rel_path
                    
                    # Create parent directories
                    dst_file.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Copy file
                    shutil.copy2(src_file, dst_file)
                    total_files += 1
                    self.stdout.write(f"✓ {rel_path}")
            
            # Verify CSS files
            css_files = list((dst / 'css').glob('*.css'))
            self.stdout.write(self.style.SUCCESS(
                f"\n✅ Successfully copied {total_files} files"
            ))
            self.stdout.write(f"✓ Found {len(css_files)} CSS files in staticfiles/css/")
            
            for css_file in css_files:
                self.stdout.write(f"  - {css_file.name}")
                
        except Exception as e:
            self.stderr.write(self.style.ERROR(f"❌ Error copying files: {e}"))
            import traceback
            traceback.print_exc()
