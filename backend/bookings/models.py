from django.db import models
from django.conf import settings
from django.utils import timezone
from django.core.exceptions import ValidationError
from rooms.models import Room, RoomType
import uuid


class Booking(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('checked_in', 'Checked In'),
        ('checked_out', 'Checked Out'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    )
    
    PAYMENT_STATUS = (
        ('unpaid', 'Unpaid'),
        ('partial', 'Partially Paid'),
        ('paid', 'Fully Paid'),
        ('refunded', 'Refunded'),
    )

    booking_reference = models.CharField(max_length=20, unique=True, editable=False)
    guest = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
                               null=True, blank=True, related_name='bookings')
    
    # Guest details for non-registered guests
    guest_name = models.CharField(max_length=100)
    guest_email = models.EmailField()
    guest_phone = models.CharField(max_length=20)
    guest_id_number = models.CharField(max_length=50, blank=True)
    guest_nationality = models.CharField(max_length=50, default='Kenyan')
    
    # Room details
    room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name='bookings')
    room_type = models.ForeignKey(RoomType, on_delete=models.PROTECT)
    
    # Booking dates
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    actual_check_in = models.DateTimeField(null=True, blank=True)
    actual_check_out = models.DateTimeField(null=True, blank=True)
    
    # Guests count
    adults = models.PositiveIntegerField(default=1)
    children = models.PositiveIntegerField(default=0)
    
    # Pricing
    nightly_rate = models.DecimalField(max_digits=10, decimal_places=2)
    total_nights = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    tax = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='unpaid')
    
    # Special requests
    special_requests = models.TextField(blank=True)
    internal_notes = models.TextField(blank=True)
    
    # Tracking
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
                                    null=True, related_name='bookings_created')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Booking'
        verbose_name_plural = 'Bookings'

    def __str__(self):
        return f'{self.booking_reference} - {self.guest_name}'

    def save(self, *args, **kwargs):
        if not self.booking_reference:
            self.booking_reference = self.generate_booking_reference()
        
        # Calculate totals
        self.total_nights = (self.check_out_date - self.check_in_date).days
        if self.total_nights < 1:
            self.total_nights = 1
        
        self.subtotal = self.nightly_rate * self.total_nights
        self.total_amount = self.subtotal - self.discount + self.tax
        
        # Update payment status
        if self.amount_paid >= self.total_amount:
            self.payment_status = 'paid'
        elif self.amount_paid > 0:
            self.payment_status = 'partial'
        
        super().save(*args, **kwargs)
    
    def generate_booking_reference(self):
        prefix = 'EH'
        date_part = timezone.now().strftime('%y%m%d')
        unique_part = uuid.uuid4().hex[:4].upper()
        return f'{prefix}{date_part}{unique_part}'
    
    def clean(self):
        if self.check_in_date and self.check_out_date:
            if self.check_out_date <= self.check_in_date:
                raise ValidationError('Check-out date must be after check-in date')
    
    @property
    def balance_due(self):
        return self.total_amount - self.amount_paid
    
    @property
    def is_past(self):
        return self.check_out_date < timezone.now().date()
    
    @property
    def is_active(self):
        return self.status in ['confirmed', 'checked_in']
    
    def check_in(self):
        self.status = 'checked_in'
        self.actual_check_in = timezone.now()
        self.room.set_occupied()
        self.save()
    
    def check_out(self):
        self.status = 'checked_out'
        self.actual_check_out = timezone.now()
        self.room.set_cleaning()
        self.save()
    
    def cancel(self):
        self.status = 'cancelled'
        if self.room.status == 'reserved':
            self.room.set_available()
        self.save()
    
    def confirm(self):
        self.status = 'confirmed'
        self.room.status = 'reserved'
        self.room.save()
        self.save()


class Payment(models.Model):
    PAYMENT_METHODS = (
        ('cash', 'Cash'),
        ('mpesa', 'M-Pesa'),
        ('card', 'Credit/Debit Card'),
        ('bank_transfer', 'Bank Transfer'),
        ('other', 'Other'),
    )

    booking = models.ForeignKey(Booking, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    transaction_reference = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    
    received_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, 
                                     null=True, related_name='payments_received')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.booking.booking_reference} - KES {self.amount}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update booking's amount_paid
        self.booking.amount_paid = sum(p.amount for p in self.booking.payments.all())
        self.booking.save()
