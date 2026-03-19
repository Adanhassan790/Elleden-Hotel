from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid


class ContactMessage(models.Model):
    """Store contact form messages"""
    SUBJECT_CHOICES = [
        ('room_booking', 'Room Booking'),
        ('restaurant', 'Restaurant Reservation'),
        ('conference', 'Conference Booking'),
        ('catering', 'Catering Inquiry'),
        ('feedback', 'Feedback'),
        ('other', 'Other'),
    ]
    STATUS_CHOICES = [
        ('new', 'New'),
        ('read', 'Read'),
        ('replied', 'Replied'),
        ('archived', 'Archived'),
    ]
    
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    subject = models.CharField(max_length=50, choices=SUBJECT_CHOICES)
    message = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} - {self.get_subject_display()}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class RestaurantReservation(models.Model):
    """Restaurant table reservations"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    MEAL_CHOICES = [
        ('breakfast', 'Breakfast (6:00 AM - 10:00 AM)'),
        ('lunch', 'Lunch (12:00 PM - 3:00 PM)'),
        ('dinner', 'Dinner (6:00 PM - 10:00 PM)'),
    ]
    
    # Booking Reference
    booking_reference = models.CharField(max_length=20, unique=True, editable=False, default='')
    
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    date = models.DateField()
    meal_time = models.CharField(max_length=20, choices=MEAL_CHOICES)
    time = models.TimeField(help_text="Preferred arrival time")
    guests = models.PositiveIntegerField()
    special_requests = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-date', '-time']
        verbose_name = 'Restaurant Reservation'
        verbose_name_plural = 'Restaurant Reservations'
    
    def __str__(self):
        return f"{self.booking_reference} - {self.name}"
    
    def save(self, *args, **kwargs):
        if not self.booking_reference:
            self.booking_reference = self.generate_reference()
        super().save(*args, **kwargs)
    
    def generate_reference(self):
        from django.utils import timezone
        prefix = 'RS'
        date_part = timezone.now().strftime('%y%m%d')
        unique_part = uuid.uuid4().hex[:4].upper()
        return f'{prefix}{date_part}{unique_part}'


class ConferenceBooking(models.Model):
    """Conference room bookings"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    PAYMENT_STATUS = [
        ('unpaid', 'Unpaid'),
        ('partial', 'Partially Paid'),
        ('paid', 'Fully Paid'),
        ('refunded', 'Refunded'),
    ]
    EVENT_TYPE_CHOICES = [
        ('meeting', 'Corporate Meeting'),
        ('training', 'Training/Workshop'),
        ('seminar', 'Seminar'),
        ('conference', 'Conference'),
        ('wedding', 'Wedding/Reception'),
        ('product_launch', 'Product Launch'),
        ('government', 'Government Session'),
        ('ngo', 'NGO Workshop'),
        ('private', 'Private Celebration'),
        ('other', 'Other'),
    ]
    PACKAGE_CHOICES = [
        ('half_day', 'Half Day (4 Hours) - KES 15,000'),
        ('full_day', 'Full Day (8 Hours) - KES 25,000'),
        ('residential', 'Residential Package - KES 5,000/person'),
        ('custom', 'Custom Package'),
    ]
    SEATING_CHOICES = [
        ('u_shape', 'U-Shape'),
        ('classroom', 'Classroom'),
        ('banquet', 'Banquet'),
        ('theatre', 'Theatre'),
        ('boardroom', 'Boardroom'),
    ]
    
    # Booking Reference
    booking_reference = models.CharField(max_length=20, unique=True, editable=False, default='')
    
    organization_name = models.CharField(max_length=200)
    contact_person = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPE_CHOICES)
    event_date = models.DateField()
    end_date = models.DateField(null=True, blank=True, help_text="For multi-day events")
    start_time = models.TimeField()
    end_time = models.TimeField()
    attendees = models.PositiveIntegerField()
    package = models.CharField(max_length=20, choices=PACKAGE_CHOICES)
    seating_arrangement = models.CharField(max_length=20, choices=SEATING_CHOICES)
    catering_required = models.BooleanField(default=True)
    av_equipment_required = models.BooleanField(default=True)
    additional_requirements = models.TextField(blank=True)
    
    # Pricing
    base_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    catering_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    equipment_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='unpaid')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-event_date']
        verbose_name = 'Conference Booking'
        verbose_name_plural = 'Conference Bookings'
    
    def __str__(self):
        return f"{self.booking_reference} - {self.organization_name}"
    
    def save(self, *args, **kwargs):
        if not self.booking_reference:
            self.booking_reference = self.generate_reference()
        self.calculate_total()
        super().save(*args, **kwargs)
    
    def generate_reference(self):
        from django.utils import timezone
        prefix = 'CF'
        date_part = timezone.now().strftime('%y%m%d')
        unique_part = uuid.uuid4().hex[:4].upper()
        return f'{prefix}{date_part}{unique_part}'
    
    def calculate_total(self):
        # Base package prices
        package_prices = {
            'half_day': 15000,
            'full_day': 25000,
            'residential': 5000 * self.attendees,
            'custom': 0,
        }
        self.base_price = package_prices.get(self.package, 0)
        
        # Catering (estimate KES 1,500 per person)
        if self.catering_required:
            self.catering_cost = 1500 * self.attendees
        
        # AV Equipment (flat KES 5,000)
        if self.av_equipment_required:
            self.equipment_cost = 5000
        
        self.total_amount = self.base_price + self.catering_cost + self.equipment_cost
        
        # Update payment status
        if self.amount_paid >= self.total_amount and self.total_amount > 0:
            self.payment_status = 'paid'
        elif self.amount_paid > 0:
            self.payment_status = 'partial'
    
    @property
    def balance_due(self):
        return self.total_amount - self.amount_paid


class CateringPackage(models.Model):
    """Fixed catering packages for quick ordering"""
    name = models.CharField(max_length=100)
    description = models.TextField()
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_guests = models.PositiveIntegerField(default=20)
    menu_items = models.TextField(help_text="List of included items")
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['price_per_person']
        verbose_name = 'Catering Package'
        verbose_name_plural = 'Catering Packages'
    
    def __str__(self):
        return f"{self.name} - KES {self.price_per_person}/person"


class CateringOrder(models.Model):
    """Catering orders with payment support"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('preparing', 'Preparing'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    PAYMENT_STATUS = [
        ('unpaid', 'Unpaid'),
        ('partial', 'Partially Paid'),
        ('paid', 'Fully Paid'),
        ('refunded', 'Refunded'),
    ]
    EVENT_TYPE_CHOICES = [
        ('corporate', 'Corporate Event'),
        ('wedding', 'Wedding'),
        ('birthday', 'Birthday Party'),
        ('government', 'Government/NGO Function'),
        ('religious', 'Religious Gathering'),
        ('family', 'Family Occasion'),
        ('other', 'Other'),
    ]
    
    # Booking Reference
    booking_reference = models.CharField(max_length=20, unique=True, editable=False, default='')
    
    # Customer Details
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    
    # Event Details
    event_type = models.CharField(max_length=50, choices=EVENT_TYPE_CHOICES)
    event_date = models.DateField()
    event_time = models.TimeField()
    venue_address = models.TextField(help_text="Event venue/location")
    guest_count = models.PositiveIntegerField()
    
    # Package Selection
    package = models.ForeignKey(CateringPackage, on_delete=models.PROTECT, null=True, blank=True)
    custom_menu = models.TextField(blank=True, help_text="Custom menu items if not using package")
    special_requests = models.TextField(blank=True)
    
    # Pricing
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=2000)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='unpaid')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-event_date']
        verbose_name = 'Catering Order'
        verbose_name_plural = 'Catering Orders'
    
    def __str__(self):
        return f"{self.booking_reference} - {self.name}"
    
    def save(self, *args, **kwargs):
        if not self.booking_reference:
            self.booking_reference = self.generate_reference()
        self.calculate_total()
        super().save(*args, **kwargs)
    
    def generate_reference(self):
        from django.utils import timezone
        prefix = 'CT'
        date_part = timezone.now().strftime('%y%m%d')
        unique_part = uuid.uuid4().hex[:4].upper()
        return f'{prefix}{date_part}{unique_part}'
    
    def calculate_total(self):
        if self.package:
            self.price_per_person = self.package.price_per_person
        
        food_cost = self.price_per_person * self.guest_count
        self.total_amount = food_cost + self.delivery_fee
        
        # Update payment status
        if self.amount_paid >= self.total_amount and self.total_amount > 0:
            self.payment_status = 'paid'
        elif self.amount_paid > 0:
            self.payment_status = 'partial'
    
    @property
    def balance_due(self):
        return self.total_amount - self.amount_paid


class CateringInquiry(models.Model):
    """Outside catering inquiries"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('quoted', 'Quote Sent'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    ]
    EVENT_TYPE_CHOICES = [
        ('corporate', 'Corporate Event'),
        ('wedding', 'Wedding'),
        ('birthday', 'Birthday Party'),
        ('government', 'Government/NGO Function'),
        ('religious', 'Religious Gathering'),
        ('family', 'Family Occasion'),
        ('other', 'Other'),
    ]
    SERVICE_TYPE_CHOICES = [
        ('buffet', 'Buffet Service'),
        ('plated', 'Plated Service'),
        ('cocktail', 'Cocktail/Finger Food'),
        ('full_service', 'Full Service (Staff included)'),
    ]
    
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    event_type = models.CharField(max_length=50, choices=EVENT_TYPE_CHOICES)
    event_date = models.DateField()
    event_time = models.TimeField()
    venue_address = models.TextField(help_text="Event venue/location")
    guest_count = models.PositiveIntegerField()
    service_type = models.CharField(max_length=50, choices=SERVICE_TYPE_CHOICES)
    menu_preferences = models.TextField(blank=True, help_text="Any specific menu items or dietary requirements")
    budget_range = models.CharField(max_length=100, blank=True, help_text="Approximate budget")
    additional_services = models.TextField(blank=True, help_text="Decorations, equipment, etc.")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-event_date']
        verbose_name = 'Catering Inquiry'
        verbose_name_plural = 'Catering Inquiries'
    
    def __str__(self):
        return f"{self.name} - {self.get_event_type_display()} on {self.event_date}"


class ServicePayment(models.Model):
    """Payment records for Conference and Catering services"""
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('mpesa', 'M-Pesa'),
        ('card', 'Credit/Debit Card'),
        ('bank_transfer', 'Bank Transfer'),
    ]
    SERVICE_TYPES = [
        ('conference', 'Conference Booking'),
        ('catering', 'Catering Order'),
    ]
    
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES)
    conference_booking = models.ForeignKey(ConferenceBooking, on_delete=models.CASCADE, 
                                           null=True, blank=True, related_name='payments')
    catering_order = models.ForeignKey(CateringOrder, on_delete=models.CASCADE,
                                       null=True, blank=True, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    transaction_reference = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_service_type_display()} - KES {self.amount}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Update the related booking's amount_paid
        if self.service_type == 'conference' and self.conference_booking:
            total = sum(p.amount for p in self.conference_booking.payments.all())
            self.conference_booking.amount_paid = total
            self.conference_booking.save()
        elif self.service_type == 'catering' and self.catering_order:
            total = sum(p.amount for p in self.catering_order.payments.all())
            self.catering_order.amount_paid = total
            self.catering_order.save()


class ServiceMpesaTransaction(models.Model):
    """M-Pesa STK Push transactions for services"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('cancelled', 'Cancelled'),
    ]
    SERVICE_TYPES = [
        ('conference', 'Conference Booking'),
        ('catering', 'Catering Order'),
    ]
    
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPES)
    conference_booking = models.ForeignKey(ConferenceBooking, on_delete=models.CASCADE,
                                           null=True, blank=True, related_name='mpesa_transactions')
    catering_order = models.ForeignKey(CateringOrder, on_delete=models.CASCADE,
                                       null=True, blank=True, related_name='mpesa_transactions')
    phone_number = models.CharField(max_length=15)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    merchant_request_id = models.CharField(max_length=100, blank=True)
    checkout_request_id = models.CharField(max_length=100, unique=True)
    mpesa_receipt_number = models.CharField(max_length=50, blank=True)
    result_code = models.IntegerField(null=True, blank=True)
    result_description = models.TextField(blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Service M-Pesa Transaction'
        verbose_name_plural = 'Service M-Pesa Transactions'
    
    def __str__(self):
        ref = self.mpesa_receipt_number or self.checkout_request_id
        return f"{self.get_service_type_display()} - {ref}"
    
    def mark_completed(self, mpesa_receipt, result_desc=''):
        """Mark transaction as completed and create Payment record"""
        self.status = 'completed'
        self.mpesa_receipt_number = mpesa_receipt
        self.result_code = 0
        self.result_description = result_desc
        self.save()
        
        # Create Payment record
        payment_data = {
            'service_type': self.service_type,
            'amount': self.amount,
            'payment_method': 'mpesa',
            'transaction_reference': mpesa_receipt,
            'notes': f'M-Pesa STK Push from {self.phone_number}'
        }
        
        if self.service_type == 'conference':
            payment_data['conference_booking'] = self.conference_booking
        else:
            payment_data['catering_order'] = self.catering_order
        
        ServicePayment.objects.create(**payment_data)
    
    def mark_failed(self, result_code, result_desc):
        """Mark transaction as failed"""
        self.status = 'failed'
        self.result_code = result_code
        self.result_description = result_desc
        self.save()


class Notification(models.Model):
    """User and Admin Notifications"""
    NOTIFICATION_TYPES = [
        ('booking', 'Booking Notification'),
        ('payment', 'Payment Notification'),
        ('booking_status', 'Booking Status Update'),
        ('cancellation', 'Cancellation Notification'),
        ('reminder', 'Reminder'),
        ('system', 'System Notification'),
        ('message', 'Message'),
        ('admin_alert', 'Admin Alert'),
    ]
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES, default='system')
    
    # Reference to related objects
    booking = models.ForeignKey('bookings.Booking', on_delete=models.SET_NULL, 
                               null=True, blank=True, related_name='notifications')
    payment = models.ForeignKey('bookings.Payment', on_delete=models.SET_NULL,
                               null=True, blank=True, related_name='notifications')
    
    # Status
    is_read = models.BooleanField(default=False)
    read_at = models.DateTimeField(null=True, blank=True)
    
    # Icon/Link
    icon = models.CharField(max_length=50, default='fa-bell', help_text="Font Awesome icon class")
    link = models.CharField(max_length=500, blank=True, help_text="URL to relevant page")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Notification'
        verbose_name_plural = 'Notifications'
    
    def __str__(self):
        return f"{self.title} - {self.user.email}"
    
    def mark_as_read(self):
        """Mark notification as read"""
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save()
    
    def mark_as_unread(self):
        """Mark notification as unread"""
        if self.is_read:
            self.is_read = False
            self.read_at = None
            self.save()
    
    @staticmethod
    def create_booking_notification(user, booking, title=None, message=None, notification_type='booking'):
        """Create booking notification"""
        title = title or f"Booking Confirmation - {booking.booking_reference}"
        message = message or f"Your booking for {booking.room_type.name} has been confirmed."
        
        return Notification.objects.create(
            user=user,
            title=title,
            message=message,
            notification_type=notification_type,
            booking=booking,
            icon='fa-calendar-check',
            link=f'/bookings/{booking.id}/'
        )
    
    @staticmethod
    def create_payment_notification(user, booking, title=None, message=None, payment=None):
        """Create payment notification"""
        title = title or f"Payment Received - {booking.booking_reference}"
        message = message or f"Payment of KES {booking.total_amount:,.0f} has been confirmed."
        
        return Notification.objects.create(
            user=user,
            title=title,
            message=message,
            notification_type='payment',
            booking=booking,
            payment=payment,
            icon='fa-credit-card',
            link=f'/bookings/{booking.id}/'
        )
    
    @staticmethod
    def create_status_notification(user, booking, old_status, new_status):
        """Create booking status change notification"""
        status_messages = {
            'confirmed': 'Your booking has been confirmed!',
            'checked_in': 'You have checked in successfully. Welcome!',
            'checked_out': 'Thank you for staying with us!',
            'cancelled': 'Your booking has been cancelled.',
        }
        
        title = f"Booking Status Update - {booking.booking_reference}"
        message = status_messages.get(new_status, f"Booking status changed to {booking.get_status_display()}")
        
        return Notification.objects.create(
            user=user,
            title=title,
            message=message,
            notification_type='booking_status',
            booking=booking,
            icon='fa-info-circle',
            link=f'/bookings/{booking.id}/'
        )
