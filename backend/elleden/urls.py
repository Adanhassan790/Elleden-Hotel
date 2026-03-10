"""
URL configuration for Elleden Hotel
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('dashboard/', include('dashboard.urls')),
    path('', include('pages.urls')),
    path('accounts/', include('accounts.urls')),
    path('rooms/', include('rooms.urls')),
    path('bookings/', include('bookings.urls')),
    path('api/', include('api.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Admin site customization
admin.site.site_header = 'Elleden Hotel Administration'
admin.site.site_title = 'Elleden Hotel Admin'
admin.site.index_title = 'Welcome to Elleden Hotel Management System'
