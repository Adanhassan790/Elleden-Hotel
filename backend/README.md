# Elleden Hotel - Backend (Django)

A Django-based backend system for Elleden Hotel (K) Limited, providing user authentication, room management, booking system, and admin dashboard.

## Features

- **User Authentication**: Customer registration, login/logout, profile management
- **Room Management**: Room types, individual rooms, availability tracking
- **Booking System**: Online reservations, booking management, payment tracking
- **Admin Dashboard**: Staff dashboard with analytics, booking management, room status
- **Customer Portal**: Personal dashboard, booking history, profile management
- **REST API**: Full API for frontend integration

## Tech Stack

- **Framework**: Django 5.0.1
- **Database**: SQLite (development) / PostgreSQL (production)
- **API**: Django REST Framework
- **Authentication**: Session-based + JWT for API
- **Frontend**: Bootstrap 5, Font Awesome

## Installation

### Prerequisites

- Python 3.10+
- pip

### Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Create environment file**:
   ```bash
   # Create .env file
   echo SECRET_KEY=your-secret-key-here > .env
   echo DEBUG=True >> .env
   ```

5. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**:
   ```bash
   python manage.py createsuperuser
   ```

7. **Seed initial data**:
   ```bash
   python manage.py seed_rooms
   ```

8. **Run development server**:
   ```bash
   python manage.py runserver
   ```

9. **Access the application**:
   - Admin Dashboard: http://127.0.0.1:8000/dashboard/admin/
   - Django Admin: http://127.0.0.1:8000/admin/
   - Customer Signup: http://127.0.0.1:8000/accounts/signup/
   - Customer Login: http://127.0.0.1:8000/accounts/login/
   - Book a Room: http://127.0.0.1:8000/bookings/book/

## Project Structure

```
backend/
├── elleden/            # Main project settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── accounts/           # User authentication
│   ├── models.py       # Custom User model
│   ├── views.py        # Auth views
│   └── forms.py        # Registration/Login forms
├── rooms/              # Room management
│   ├── models.py       # RoomType, Room models
│   └── admin.py        # Admin configuration
├── bookings/           # Booking system
│   ├── models.py       # Booking, Payment models
│   ├── views.py        # Booking views
│   └── forms.py        # Booking forms
├── dashboard/          # Admin & Customer dashboards
│   ├── views.py        # Dashboard views
│   └── urls.py         # Dashboard routes
├── api/                # REST API
│   ├── serializers.py  # DRF serializers
│   ├── views.py        # API views
│   └── urls.py         # API routes
├── templates/          # HTML templates
└── static/             # Static files
```

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new customer
- `POST /api/auth/login/` - Get JWT tokens
- `POST /api/auth/refresh/` - Refresh JWT token
- `GET /api/auth/profile/` - Get user profile

### Rooms
- `GET /api/rooms/` - List room types
- `GET /api/rooms/<id>/` - Room type detail
- `GET /api/rooms/availability/` - Check availability

### Bookings
- `POST /api/bookings/` - Create booking
- `GET /api/bookings/my-bookings/` - Customer's bookings
- `GET /api/bookings/<id>/` - Booking detail
- `POST /api/bookings/<id>/cancel/` - Cancel booking

## User Types

1. **Customer** - Regular guests who can book rooms
2. **Staff** - Hotel staff with limited access
3. **Manager** - Hotel managers with more permissions
4. **Admin** - Full access to all features

## Room Types & Pricing

| Room Type    | Price (KES) | Max Occupancy |
|-------------|-------------|---------------|
| Single Room | 3,500       | 1             |
| Double Room | 5,000       | 2             |
| Twin Room   | 5,500       | 2             |
| Family Suite| 7,500       | 4             |

## Production Deployment

1. Set `DEBUG=False` in .env
2. Configure `ALLOWED_HOSTS`
3. Use PostgreSQL database
4. Set up proper email backend
5. Configure CORS for your domain
6. Run `python manage.py collectstatic`
7. Use gunicorn with nginx

## Contact

Elleden Hotel (K) Limited
- Address: Moyale Road, Marsabit Town, Kenya
- Phone: +254 759 435 880
- Email: info@elledenhotel.co.ke
