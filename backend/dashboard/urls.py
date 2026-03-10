from django.urls import path
from . import views
from pages.views import home

app_name = 'dashboard'

urlpatterns = [
    # Home redirect
    path('', home, name='home'),
    
    # Admin Dashboard
    path('admin/', views.admin_dashboard, name='admin_index'),
    
    # Room Bookings Management
    path('admin/bookings/', views.booking_management, name='bookings'),
    path('admin/bookings/<int:pk>/', views.booking_detail, name='booking_detail'),
    path('admin/bookings/<int:pk>/<str:action>/', views.booking_action, name='booking_action'),
    
    # Room Management
    path('admin/rooms/', views.room_management, name='rooms'),
    path('admin/rooms/<int:pk>/status/<str:status>/', views.room_status_update, name='room_status'),
    
    # Conference Management
    path('admin/conferences/', views.conference_management, name='conferences'),
    path('admin/conferences/<int:pk>/', views.conference_detail, name='conference_detail'),
    path('admin/conferences/<int:pk>/<str:action>/', views.conference_action, name='conference_action'),
    
    # Catering Management
    path('admin/catering/', views.catering_management, name='catering'),
    path('admin/catering/<int:pk>/', views.catering_detail, name='catering_detail'),
    path('admin/catering/<int:pk>/<str:action>/', views.catering_action, name='catering_action'),
    
    # Restaurant Reservations Management
    path('admin/restaurant/', views.restaurant_management, name='restaurant'),
    path('admin/restaurant/<int:pk>/<str:action>/', views.restaurant_action, name='restaurant_action'),
    
    # Payments Management
    path('admin/payments/', views.payments_management, name='payments'),
    
    # Guests Management
    path('admin/guests/', views.guest_management, name='guests'),
    
    # Reports
    path('admin/reports/', views.reports_dashboard, name='reports'),
    
    # API Endpoints
    path('api/stats/', views.api_dashboard_stats, name='api_stats'),
    
    # Customer Dashboard
    path('customer/', views.customer_dashboard, name='customer_index'),
]
