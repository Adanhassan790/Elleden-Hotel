from django.db import models
from django.utils import timezone


class RoomType(models.Model):
    name = models.CharField(max_length=50)  # Single, Double, Twin, Family
    description = models.TextField()
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    max_occupancy = models.PositiveIntegerField(default=2)
    image = models.ImageField(upload_to='room_types/', blank=True, null=True)
    
    # Amenities
    has_wifi = models.BooleanField(default=True)
    has_tv = models.BooleanField(default=True)
    has_ac = models.BooleanField(default=False)
    has_minibar = models.BooleanField(default=False)
    has_workspace = models.BooleanField(default=False)
    has_ensuite = models.BooleanField(default=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['base_price']
        verbose_name = 'Room Type'
        verbose_name_plural = 'Room Types'

    def __str__(self):
        return f'{self.name} - KES {self.base_price}'
    
    def get_amenities(self):
        amenities = []
        if self.has_wifi:
            amenities.append('Wi-Fi')
        if self.has_tv:
            amenities.append('TV')
        if self.has_ac:
            amenities.append('Air Conditioning')
        if self.has_minibar:
            amenities.append('Minibar')
        if self.has_workspace:
            amenities.append('Work Desk')
        if self.has_ensuite:
            amenities.append('En-suite Bathroom')
        return amenities


class Room(models.Model):
    STATUS_CHOICES = (
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('maintenance', 'Under Maintenance'),
        ('cleaning', 'Being Cleaned'),
        ('reserved', 'Reserved'),
    )

    room_number = models.CharField(max_length=10, unique=True)
    room_type = models.ForeignKey(RoomType, on_delete=models.PROTECT, related_name='rooms')
    floor = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    notes = models.TextField(blank=True)
    
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['room_number']
        verbose_name = 'Room'
        verbose_name_plural = 'Rooms'

    def __str__(self):
        return f'Room {self.room_number} ({self.room_type.name})'

    @property
    def is_available(self):
        return self.status == 'available'
    
    def set_occupied(self):
        self.status = 'occupied'
        self.save()
    
    def set_available(self):
        self.status = 'available'
        self.save()
    
    def set_cleaning(self):
        self.status = 'cleaning'
        self.save()


class RoomImage(models.Model):
    room_type = models.ForeignKey(RoomType, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='room_images/')
    caption = models.CharField(max_length=100, blank=True)
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_primary', '-uploaded_at']

    def __str__(self):
        return f'{self.room_type.name} - {self.caption or "Image"}'
