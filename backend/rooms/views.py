from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.http import JsonResponse
from django.utils import timezone
from datetime import datetime, timedelta
from .models import RoomType, Room
from bookings.models import Booking


class RoomTypeListView(ListView):
    model = RoomType
    template_name = 'rooms/room_list.html'
    context_object_name = 'room_types'
    
    def get_queryset(self):
        return RoomType.objects.filter(is_active=True)


class RoomTypeDetailView(DetailView):
    model = RoomType
    template_name = 'rooms/room_detail.html'
    context_object_name = 'room_type'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['available_rooms'] = self.object.rooms.filter(status='available', is_active=True)
        return context


class AvailabilityCalendarView(TemplateView):
    """View for room availability calendar"""
    template_name = 'rooms/availability_calendar.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['room_types'] = RoomType.objects.filter(is_active=True)
        return context


def get_availability_data(request):
    """AJAX endpoint for calendar data"""
    room_type_id = request.GET.get('room_type')
    start = request.GET.get('start')
    end = request.GET.get('end')
    
    if start:
        start_date = datetime.strptime(start[:10], '%Y-%m-%d').date()
    else:
        start_date = timezone.now().date()
    
    if end:
        end_date = datetime.strptime(end[:10], '%Y-%m-%d').date()
    else:
        end_date = start_date + timedelta(days=30)
    
    room_types = RoomType.objects.filter(is_active=True)
    if room_type_id:
        room_types = room_types.filter(pk=room_type_id)
    
    events = []
    
    for room_type in room_types:
        total_rooms = Room.objects.filter(
            room_type=room_type,
            is_active=True
        ).count()
        
        current_date = start_date
        while current_date <= end_date:
            booked = Booking.objects.filter(
                room_type=room_type,
                check_in_date__lte=current_date,
                check_out_date__gt=current_date,
                status__in=['confirmed', 'checked_in', 'pending']
            ).count()
            
            available = total_rooms - booked
            
            if available > 0:
                color = '#28a745'  # Green - available
                title = f'{room_type.name}: {available} available'
            else:
                color = '#dc3545'  # Red - full
                title = f'{room_type.name}: FULL'
            
            events.append({
                'title': title,
                'start': current_date.strftime('%Y-%m-%d'),
                'color': color,
                'extendedProps': {
                    'room_type': room_type.name,
                    'available': available,
                    'total': total_rooms,
                    'price': str(room_type.base_price)
                }
            })
            
            current_date += timedelta(days=1)
    
    return JsonResponse(events, safe=False)
