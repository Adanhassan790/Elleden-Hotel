from django.db import models


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
        return f"{self.name} - {self.date} ({self.guests} guests)"


class ConferenceBooking(models.Model):
    """Conference room bookings"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
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
        ('half_day', 'Half Day (4 Hours)'),
        ('full_day', 'Full Day (8 Hours)'),
        ('residential', 'Residential (Multi-day)'),
        ('custom', 'Custom Package'),
    ]
    SEATING_CHOICES = [
        ('u_shape', 'U-Shape'),
        ('classroom', 'Classroom'),
        ('banquet', 'Banquet'),
        ('theatre', 'Theatre'),
        ('boardroom', 'Boardroom'),
    ]
    
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
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-event_date']
        verbose_name = 'Conference Booking'
        verbose_name_plural = 'Conference Bookings'
    
    def __str__(self):
        return f"{self.organization_name} - {self.event_date}"


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
