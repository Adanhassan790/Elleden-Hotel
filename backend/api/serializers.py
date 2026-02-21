from rest_framework import serializers
from accounts.models import User
from rooms.models import RoomType, Room, RoomImage
from bookings.models import Booking, Payment


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'user_type']
        read_only_fields = ['id', 'email', 'user_type']


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)
    password_confirm = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'phone', 'password', 'password_confirm']
    
    def validate(self, data):
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({'password_confirm': 'Passwords do not match'})
        return data
    
    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
            phone=validated_data.get('phone', ''),
            user_type='customer'
        )
        return user


class RoomImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = RoomImage
        fields = ['id', 'image', 'caption', 'is_primary']


class RoomTypeSerializer(serializers.ModelSerializer):
    images = RoomImageSerializer(many=True, read_only=True)
    amenities = serializers.SerializerMethodField()
    available_count = serializers.SerializerMethodField()
    
    class Meta:
        model = RoomType
        fields = ['id', 'name', 'description', 'base_price', 'max_occupancy', 
                  'image', 'amenities', 'images', 'available_count']
    
    def get_amenities(self, obj):
        return obj.get_amenities()
    
    def get_available_count(self, obj):
        return obj.rooms.filter(status='available', is_active=True).count()


class RoomSerializer(serializers.ModelSerializer):
    room_type_name = serializers.CharField(source='room_type.name', read_only=True)
    price = serializers.DecimalField(source='room_type.base_price', max_digits=10, 
                                      decimal_places=2, read_only=True)
    
    class Meta:
        model = Room
        fields = ['id', 'room_number', 'room_type', 'room_type_name', 'floor', 
                  'status', 'price', 'is_available']


class BookingSerializer(serializers.ModelSerializer):
    room_type_name = serializers.CharField(source='room_type.name', read_only=True)
    room_number = serializers.CharField(source='room.room_number', read_only=True)
    
    class Meta:
        model = Booking
        fields = ['id', 'booking_reference', 'guest_name', 'guest_email', 'guest_phone',
                  'room_type', 'room_type_name', 'room_number', 'check_in_date', 
                  'check_out_date', 'adults', 'children', 'total_nights', 'nightly_rate',
                  'total_amount', 'status', 'payment_status', 'special_requests', 
                  'created_at']
        read_only_fields = ['id', 'booking_reference', 'room_number', 'total_nights', 
                            'total_amount', 'status', 'payment_status', 'created_at']


class BookingCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = ['guest_name', 'guest_email', 'guest_phone', 'room_type',
                  'check_in_date', 'check_out_date', 'adults', 'children', 
                  'special_requests']
    
    def validate(self, data):
        if data['check_out_date'] <= data['check_in_date']:
            raise serializers.ValidationError('Check-out date must be after check-in date')
        return data


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'amount', 'payment_method', 'transaction_reference', 
                  'created_at']
        read_only_fields = ['id', 'created_at']
