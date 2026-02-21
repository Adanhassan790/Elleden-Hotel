from django.urls import path
from . import views

app_name = 'rooms'

urlpatterns = [
    path('', views.RoomTypeListView.as_view(), name='list'),
    path('availability/', views.AvailabilityCalendarView.as_view(), name='availability_calendar'),
    path('availability/data/', views.get_availability_data, name='availability_data'),
    path('<int:pk>/', views.RoomTypeDetailView.as_view(), name='detail'),
]
