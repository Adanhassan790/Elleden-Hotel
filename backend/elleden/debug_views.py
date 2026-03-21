"""Debug views for troubleshooting static files"""
from django.http import JsonResponse
from django.conf import settings
from pathlib import Path
import os

def static_files_debug(request):
    """Debug endpoint to show static file configuration and available files"""
    
    debug_info = {
        "STATIC_URL": settings.STATIC_URL,
        "STATIC_ROOT": str(settings.STATIC_ROOT),
        "STATICFILES_DIRS": [str(d) for d in settings.STATICFILES_DIRS],
        "static_root_exists": settings.STATIC_ROOT.exists(),
        "static_root_is_dir": settings.STATIC_ROOT.is_dir(),
    }
    
    # Check if staticfiles/css/ exists and list files
    css_dir = settings.STATIC_ROOT / 'css'
    if css_dir.exists():
        debug_info['css_files'] = [f.name for f in css_dir.glob('*.css')]
    else:
        debug_info['css_dir_exists'] = False
    
    # Check if source static/ directory exists
    source_static = settings.STATICFILES_DIRS[0] if settings.STATICFILES_DIRS else None
    if source_static:
        debug_info['source_static'] = str(source_static)
        debug_info['source_static_exists'] = os.path.exists(source_static)
        if os.path.exists(source_static):
            css_source = Path(source_static) / 'css'
            if css_source.exists():
                debug_info['source_css_files'] = [f.name for f in css_source.glob('*.css')]
    
    return JsonResponse(debug_info, indent=2)
