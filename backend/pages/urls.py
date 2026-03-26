from django.urls import path
from . import views

app_name = 'pages'

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('rooms/', views.rooms, name='rooms'),
    path('restaurant/', views.restaurant, name='restaurant'),
    path('restaurant/confirmation/<int:pk>/', views.restaurant_confirmation, name='restaurant_confirmation'),
    path('conference/', views.conference, name='conference'),
    path('conference/confirmation/<int:pk>/', views.conference_confirmation, name='conference_confirmation'),
    path('catering/', views.catering, name='catering'),
    path('catering/confirmation/<int:pk>/', views.catering_confirmation, name='catering_confirmation'),
    path('contact/', views.contact, name='contact'),
    
    # Manual Payment URLs (Non-automated M-Pesa)
    path('payment/<str:service_type>/<int:pk>/', views.manual_service_payment, name='service_payment'),
]
