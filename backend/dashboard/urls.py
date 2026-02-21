from django.urls import path
from . import views
from pages.views import home

app_name = 'dashboard'

urlpatterns = [
    # Home redirect
    path('', home, name='home'),
    
    # Admin Dashboard
    path('admin/', views.admin_dashboard, name='admin_index'),
    path('admin/bookings/', views.booking_management, name='bookings'),
    path('admin/bookings/<int:pk>/', views.booking_detail, name='booking_detail'),
    path('admin/bookings/<int:pk>/<str:action>/', views.booking_action, name='booking_action'),
    path('admin/rooms/', views.room_management, name='rooms'),
    path('admin/rooms/<int:pk>/status/<str:status>/', views.room_status_update, name='room_status'),
    path('admin/guests/', views.guest_management, name='guests'),
    path('admin/reports/', views.reports_dashboard, name='reports'),
    
    # Customer Dashboard
    path('customer/', views.customer_dashboard, name='customer_index'),
]
