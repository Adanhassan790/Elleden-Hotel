from django.urls import path
from . import views

app_name = 'bookings'

urlpatterns = [
    path('book/', views.BookingCreateView.as_view(), name='book'),
    path('book/', views.BookingCreateView.as_view(), name='create'),
    path('confirmation/<int:pk>/', views.BookingConfirmationView.as_view(), name='confirmation'),
    path('my-bookings/', views.CustomerBookingListView.as_view(), name='my_bookings'),
    path('my-bookings/', views.CustomerBookingListView.as_view(), name='customer_list'),
    path('my-bookings/<int:pk>/', views.CustomerBookingDetailView.as_view(), name='booking_detail'),
    path('my-bookings/<int:pk>/', views.CustomerBookingDetailView.as_view(), name='customer_detail'),
    path('my-bookings/<int:pk>/cancel/', views.cancel_booking, name='cancel'),
    path('check-availability/', views.check_availability, name='check_availability'),
    
    # M-Pesa Payment URLs
    path('payment/<int:pk>/', views.initiate_mpesa_payment, name='payment'),
    path('payment/<int:pk>/status/<str:checkout_id>/', views.payment_status, name='payment_status'),
    path('payment/check-status/<str:checkout_id>/', views.check_payment_status, name='check_payment_status'),
    path('mpesa/callback/', views.mpesa_callback, name='mpesa_callback'),
]
