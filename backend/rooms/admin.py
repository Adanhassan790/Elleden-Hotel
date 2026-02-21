from django.contrib import admin
from .models import RoomType, Room, RoomImage


class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1


@admin.register(RoomType)
class RoomTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_price', 'max_occupancy', 'is_active', 'room_count')
    list_filter = ('is_active', 'has_wifi', 'has_ac')
    search_fields = ('name', 'description')
    inlines = [RoomImageInline]
    
    fieldsets = (
        (None, {'fields': ('name', 'description', 'base_price', 'max_occupancy', 'image')}),
        ('Amenities', {'fields': ('has_wifi', 'has_tv', 'has_ac', 'has_minibar', 'has_workspace', 'has_ensuite')}),
        ('Status', {'fields': ('is_active',)}),
    )
    
    def room_count(self, obj):
        return obj.rooms.count()
    room_count.short_description = 'Number of Rooms'


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('room_number', 'room_type', 'floor', 'status', 'is_active')
    list_filter = ('status', 'room_type', 'floor', 'is_active')
    search_fields = ('room_number', 'notes')
    list_editable = ('status',)
    
    fieldsets = (
        (None, {'fields': ('room_number', 'room_type', 'floor')}),
        ('Status', {'fields': ('status', 'is_active')}),
        ('Notes', {'fields': ('notes',)}),
    )


@admin.register(RoomImage)
class RoomImageAdmin(admin.ModelAdmin):
    list_display = ('room_type', 'caption', 'is_primary', 'uploaded_at')
    list_filter = ('room_type', 'is_primary')
