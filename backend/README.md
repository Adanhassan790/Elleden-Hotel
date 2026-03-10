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

## M-Pesa Payment Integration

The system includes M-Pesa STK Push (Lipa Na M-Pesa) for online payments.

### Setup

1. **Get Daraja API Credentials**
   - Register at [Safaricom Developer Portal](https://developer.safaricom.co.ke)
   - Create a new app and get Consumer Key & Secret
   - For production, apply for Go Live

2. **Configure Environment Variables**
   ```env
   MPESA_ENVIRONMENT=sandbox  # or 'production'
   MPESA_CONSUMER_KEY=your-consumer-key
   MPESA_CONSUMER_SECRET=your-consumer-secret
   MPESA_SHORTCODE=174379  # Your paybill number
   MPESA_PASSKEY=your-passkey
   MPESA_CALLBACK_URL=https://your-domain.com/bookings/mpesa/callback/
   ```

3. **For Local Testing**
   - Use [ngrok](https://ngrok.com) to expose your local server
   - Run: `ngrok http 8000`
   - Set `MPESA_CALLBACK_URL` to your ngrok URL

### Payment Flow
1. Guest makes a booking
2. Guest clicks "Pay with M-Pesa" on confirmation page
3. Enters phone number and amount
4. Receives STK push prompt on phone
5. Enters M-Pesa PIN
6. Payment confirmed and booking status updated

### Sandbox Testing
- Use test phone number: 254708374149
- M-Pesa PIN: Any 4 digits

## Production Deployment (Railway)

### Quick Deploy to Railway

1. **Create Railway Account**
   - Go to [Railway](https://railway.app) and sign up
   - Connect your GitHub account

2. **Deploy from GitHub**
   - Click "New Project" → "Deploy from GitHub repo"
   - Select your repository
   - Railway auto-detects Django and deploys

3. **Add PostgreSQL Database**
   - In your project, click "+ Add" → "Database" → "PostgreSQL"
   - Railway automatically sets `DATABASE_URL`

4. **Set Environment Variables**
   Go to "Variables" tab and add:
   ```
   SECRET_KEY=<generate-secure-key>
   DEBUG=False
   ALLOWED_HOSTS=<your-app>.up.railway.app
   MPESA_ENVIRONMENT=production
   MPESA_CONSUMER_KEY=<your-key>
   MPESA_CONSUMER_SECRET=<your-secret>
   MPESA_SHORTCODE=<your-paybill>
   MPESA_PASSKEY=<your-passkey>
   MPESA_CALLBACK_URL=https://<your-app>.up.railway.app/bookings/mpesa/callback/
   AFRICASTALKING_USERNAME=<your-username>
   AFRICASTALKING_API_KEY=<your-api-key>
   AFRICASTALKING_SENDER_ID=<your-sender-id>
   ```

5. **Generate Domain**
   - Go to "Settings" → "Networking" → "Generate Domain"
   - Your app will be live at `https://<your-app>.up.railway.app`

6. **Create Admin User**
   - Go to Railway project → Settings → Run command:
   ```bash
   python manage.py createsuperuser
   ```

### Post-Deployment Steps

1. **Seed Room Data**
   ```bash
   python manage.py seed_rooms
   ```

2. **Update M-Pesa Callback URL**
   - Go to Safaricom Developer Portal
   - Update callback URL to: `https://<your-app>.up.railway.app/bookings/mpesa/callback/`

3. **Test SMS Integration**
   - Switch Africa's Talking to production mode
   - Test with a real phone number

### Production Checklist

- [ ] DEBUG=False
- [ ] Strong SECRET_KEY generated
- [ ] PostgreSQL database connected
- [ ] M-Pesa Go Live credentials
- [ ] Africa's Talking production credentials
- [ ] SSL/HTTPS enabled (automatic on Railway)
- [ ] Custom domain configured (optional)

## Contact

Elleden Hotel (K) Limited
- Address: Moyale Road, Marsabit Town, Kenya
- Phone: +254 759 435 880
- Email: info@elledenhotel.co.ke
