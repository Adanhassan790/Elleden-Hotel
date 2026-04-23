"""
URL configuration for Elleden Hotel
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.http import JsonResponse
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView
from elleden.debug_views import static_files_debug
from elleden.sitemap import StaticViewSitemap, RoomSitemap

sitemaps = {
    'static': StaticViewSitemap,
    'rooms': RoomSitemap,
}

urlpatterns = [
    path('healthcheck/', lambda r: JsonResponse({'status': 'ok', 'DEBUG': settings.DEBUG, 'ALLOWED_HOSTS': settings.ALLOWED_HOSTS}), name='healthcheck'),
    path('admin/', admin.site.urls),
    path('robots.txt', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots.txt'),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('dashboard/', include('dashboard.urls')),
    path('', include('pages.urls')),
    path('accounts/', include('accounts.urls')),
    path('rooms/', include('rooms.urls')),
    path('bookings/', include('bookings.urls')),
    path('api/', include('api.urls')),
    # Debug endpoint
    path('debug/static-files/', static_files_debug, name='debug_static_files'),
]

# Serve static files with proper MIME types
# Use Django's serve view directly with correct settings
if not settings.DEBUG:
    # In production, explicitly serve static files with proper MIME types
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', serve, {'document_root': settings.STATIC_ROOT}, name='static'),
        re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}, name='media'),
    ]
else:
    # In development, use the standard static() helper
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Admin site customization
admin.site.site_header = 'Elleden Hotel Administration'
admin.site.site_title = 'Elleden Hotel Admin'
admin.site.index_title = 'Welcome to Elleden Hotel Management System'

# Custom error handlers
handler400 = 'elleden.error_handlers.custom_400_error'
handler404 = 'elleden.error_handlers.custom_404_error'
handler500 = 'elleden.error_handlers.custom_500_error'
