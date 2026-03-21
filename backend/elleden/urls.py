"""
URL configuration for Elleden Hotel
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from elleden.debug_views import static_files_debug

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('', include('pages.urls')),
    path('accounts/', include('accounts.urls')),
    path('rooms/', include('rooms.urls')),
    path('bookings/', include('bookings.urls')),
    path('api/', include('api.urls')),
    # Debug endpoint
    path('debug/static-files/', static_files_debug, name='debug_static_files'),
]

# Serve static and media files
# In production: WhiteNoise (WSGI) is primary, Django routes are fallback
# In development: Django routes serve directly
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
