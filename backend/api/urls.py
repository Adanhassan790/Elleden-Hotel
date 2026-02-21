from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views

app_name = 'api'

urlpatterns = [
    # Authentication
    path('auth/register/', views.RegisterView.as_view(), name='register'),
    path('auth/login/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/profile/', views.ProfileView.as_view(), name='profile'),
    
    # Rooms
    path('rooms/', views.RoomTypeListView.as_view(), name='room_list'),
    path('rooms/<int:pk>/', views.RoomTypeDetailView.as_view(), name='room_detail'),
    path('rooms/availability/', views.CheckAvailabilityView.as_view(), name='check_availability'),
    path('rooms/calendar/', views.RoomAvailabilityCalendarView.as_view(), name='availability_calendar'),
    
    # Bookings
    path('bookings/', views.BookingCreateView.as_view(), name='booking_create'),
    path('bookings/my-bookings/', views.CustomerBookingListView.as_view(), name='customer_bookings'),
    path('bookings/<int:pk>/', views.CustomerBookingDetailView.as_view(), name='booking_detail'),
    path('bookings/<int:pk>/cancel/', views.CancelBookingView.as_view(), name='booking_cancel'),
]
