from rest_framework import viewsets, generics, status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from django.db.models import Q
from datetime import datetime, timedelta

from accounts.models import User
from rooms.models import RoomType, Room
from bookings.models import Booking

from .serializers import (
    UserSerializer, UserRegistrationSerializer,
    RoomTypeSerializer, RoomSerializer,
    BookingSerializer, BookingCreateSerializer
)


class RegisterView(generics.CreateAPIView):
    """API endpoint for user registration"""
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [permissions.AllowAny]


class ProfileView(generics.RetrieveUpdateAPIView):
    """API endpoint for viewing/updating user profile"""
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user


class RoomTypeListView(generics.ListAPIView):
    """API endpoint to list all room types"""
    queryset = RoomType.objects.filter(is_active=True)
    serializer_class = RoomTypeSerializer
    permission_classes = [permissions.AllowAny]


class RoomTypeDetailView(generics.RetrieveAPIView):
    """API endpoint to get room type details"""
    queryset = RoomType.objects.filter(is_active=True)
    serializer_class = RoomTypeSerializer
    permission_classes = [permissions.AllowAny]


class CheckAvailabilityView(APIView):
    """API endpoint to check room availability"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        room_type_id = request.query_params.get('room_type')
        check_in = request.query_params.get('check_in')
        check_out = request.query_params.get('check_out')
        
        if not all([room_type_id, check_in, check_out]):
            return Response({
                'error': 'Please provide room_type, check_in, and check_out parameters'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            room_type = RoomType.objects.get(pk=room_type_id, is_active=True)
        except RoomType.DoesNotExist:
            return Response({
                'error': 'Invalid room type'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Find available rooms
        available_rooms = Room.objects.filter(
            room_type=room_type,
            status='available',
            is_active=True
        ).exclude(
            bookings__check_in_date__lt=check_out,
            bookings__check_out_date__gt=check_in,
            bookings__status__in=['confirmed', 'checked_in']
        )
        
        return Response({
            'available': available_rooms.exists(),
            'room_type': RoomTypeSerializer(room_type).data,
            'available_count': available_rooms.count()
        })


class BookingCreateView(generics.CreateAPIView):
    """API endpoint to create a new booking"""
    serializer_class = BookingCreateSerializer
    permission_classes = [permissions.AllowAny]
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        room_type = serializer.validated_data['room_type']
        check_in = serializer.validated_data['check_in_date']
        check_out = serializer.validated_data['check_out_date']
        
        # Find available room
        available_room = Room.objects.filter(
            room_type=room_type,
            status='available',
            is_active=True
        ).exclude(
            bookings__check_in_date__lt=check_out,
            bookings__check_out_date__gt=check_in,
            bookings__status__in=['confirmed', 'checked_in']
        ).first()
        
        if not available_room:
            return Response({
                'error': 'No rooms available for the selected dates'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create booking
        booking = Booking.objects.create(
            room=available_room,
            room_type=room_type,
            nightly_rate=room_type.base_price,
            guest=request.user if request.user.is_authenticated else None,
            **serializer.validated_data
        )
        
        return Response(
            BookingSerializer(booking).data,
            status=status.HTTP_201_CREATED
        )


class CustomerBookingListView(generics.ListAPIView):
    """API endpoint to list customer's bookings"""
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Booking.objects.filter(guest=self.request.user)


class CustomerBookingDetailView(generics.RetrieveAPIView):
    """API endpoint to get customer's booking detail"""
    serializer_class = BookingSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        return Booking.objects.filter(guest=self.request.user)


class CancelBookingView(APIView):
    """API endpoint to cancel a booking"""
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        try:
            booking = Booking.objects.get(pk=pk, guest=request.user)
        except Booking.DoesNotExist:
            return Response({
                'error': 'Booking not found'
            }, status=status.HTTP_404_NOT_FOUND)
        
        if booking.status not in ['pending', 'confirmed']:
            return Response({
                'error': 'This booking cannot be cancelled'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        booking.cancel()
        
        return Response({
            'message': 'Booking cancelled successfully',
            'booking': BookingSerializer(booking).data
        })


class RoomAvailabilityCalendarView(APIView):
    """API endpoint to get room availability calendar data"""
    permission_classes = [permissions.AllowAny]
    
    def get(self, request):
        room_type_id = request.query_params.get('room_type')
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        
        # Default to current month if not provided
        if not start_date:
            start_date = timezone.now().date()
        else:
            start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        
        if not end_date:
            end_date = start_date + timedelta(days=30)
        else:
            end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        # Get room type filter
        room_types = RoomType.objects.filter(is_active=True)
        if room_type_id:
            room_types = room_types.filter(pk=room_type_id)
        
        calendar_data = []
        
        for room_type in room_types:
            total_rooms = Room.objects.filter(
                room_type=room_type,
                status='available',
                is_active=True
            ).count()
            
            # Get availability for each day
            current_date = start_date
            daily_availability = []
            
            while current_date <= end_date:
                # Count booked rooms for this date
                booked_rooms = Booking.objects.filter(
                    room_type=room_type,
                    check_in_date__lte=current_date,
                    check_out_date__gt=current_date,
                    status__in=['confirmed', 'checked_in']
                ).count()
                
                available = total_rooms - booked_rooms
                
                daily_availability.append({
                    'date': current_date.strftime('%Y-%m-%d'),
                    'available': available,
                    'total': total_rooms,
                    'booked': booked_rooms,
                    'status': 'available' if available > 0 else 'full'
                })
                
                current_date += timedelta(days=1)
            
            calendar_data.append({
                'room_type': RoomTypeSerializer(room_type).data,
                'availability': daily_availability
            })
        
        return Response({
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'calendar': calendar_data
        })
