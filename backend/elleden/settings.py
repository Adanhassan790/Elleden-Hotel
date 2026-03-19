"""
Django settings for Elleden Hotel Management System
"""
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')
if not SECRET_KEY:
    raise ValueError('SECRET_KEY environment variable is not set. Set it before running the app.')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG', 'True') == 'True'

# Allowed hosts - add your production domain
ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS', 'localhost,127.0.0.1,*').split(',') + ['.railway.app', '.up.railway.app']

# =============================================================================
# PRODUCTION SECURITY SETTINGS
# =============================================================================
if not DEBUG:
    # HTTPS settings
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    
    # HSTS settings
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    
    # Additional security
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = 'DENY'

# Application definition
INSTALLED_APPS = [
    'jazzmin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    # Third party apps
    'rest_framework',
    'corsheaders',
    'crispy_forms',
    'crispy_bootstrap5',
    
    # Local apps
    'accounts',
    'rooms',
    'bookings',
    'dashboard',
    'api',
    'pages',
]

# Jazzmin Admin Settings
JAZZMIN_SETTINGS = {
    # Title and branding
    "site_title": "Elleden Hotel Admin",
    "site_header": "Elleden Hotel",
    "site_brand": "Elleden Hotel",
    "site_logo": None,
    "login_logo": None,
    "login_logo_dark": None,
    "site_logo_classes": "img-circle",
    "site_icon": None,
    "welcome_sign": "Welcome to Elleden Hotel Management System",
    "copyright": "Elleden Hotel (K) Limited",
    "search_model": ["bookings.Booking", "accounts.User", "rooms.Room", "pages.ConferenceBooking", "pages.CateringOrder"],
    "user_avatar": None,
    
    # Top Menu - Links to custom dashboard
    "topmenu_links": [
        {"name": "Dashboard", "url": "/dashboard/admin/", "icon": "fas fa-tachometer-alt"},
        {"name": "Website", "url": "/", "new_window": True, "icon": "fas fa-globe"},
    ],
    
    # Side Menu
    "show_sidebar": True,
    "navigation_expanded": True,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": ["accounts", "rooms", "bookings", "pages"],
    
    # Custom links in sidebar
    "custom_links": {
        "bookings": [{
            "name": "Analytics Dashboard",
            "url": "/dashboard/admin/",
            "icon": "fas fa-chart-line",
            "permissions": ["bookings.view_booking"]
        }],
    },
    
    # Icons
    "icons": {
        "auth": "fas fa-users-cog",
        "accounts.user": "fas fa-user",
        "accounts.User": "fas fa-user",
        "bookings.booking": "fas fa-calendar-check",
        "bookings.Booking": "fas fa-calendar-check",
        "bookings.payment": "fas fa-credit-card",
        "bookings.Payment": "fas fa-credit-card",
        "bookings.mpesatransaction": "fas fa-mobile-alt",
        "bookings.MpesaTransaction": "fas fa-mobile-alt",
        "rooms.room": "fas fa-door-open",
        "rooms.Room": "fas fa-door-open",
        "rooms.roomtype": "fas fa-bed",
        "rooms.RoomType": "fas fa-bed",
        "rooms.roomimage": "fas fa-image",
        "rooms.RoomImage": "fas fa-image",
        "pages.conferencebooking": "fas fa-users",
        "pages.ConferenceBooking": "fas fa-users",
        "pages.cateringorder": "fas fa-utensils",
        "pages.CateringOrder": "fas fa-utensils",
        "pages.cateringpackage": "fas fa-box",
        "pages.CateringPackage": "fas fa-box",
        "pages.restaurantreservation": "fas fa-concierge-bell",
        "pages.RestaurantReservation": "fas fa-concierge-bell",
        "pages.servicepayment": "fas fa-money-bill",
        "pages.ServicePayment": "fas fa-money-bill",
        "pages.servicempesatransaction": "fas fa-mobile-alt",
        "pages.ServiceMpesaTransaction": "fas fa-mobile-alt",
        "pages.contactinquiry": "fas fa-envelope",
        "pages.ContactInquiry": "fas fa-envelope",
    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    
    # Related Modal
    "related_modal_active": True,
    
    # UI Customizations
    "custom_css": "css/admin_custom.css",
    "custom_js": None,
    "use_google_fonts_cdn": True,
    "show_ui_builder": False,
    
    # Change view
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": {
        "bookings.booking": "vertical_tabs",
        "accounts.user": "collapsible",
    },
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-dark",
    "accent": "accent-warning",
    "navbar": "navbar-dark",
    "no_navbar_border": True,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-dark-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": False,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": False,
    "theme": "default",
    "dark_mode_theme": "darkly",
    "button_classes": {
        "primary": "btn-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-info",
        "warning": "btn-warning",
        "danger": "btn-danger",
        "success": "btn-success"
    },
    "actions_sticky_top": True,
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'elleden.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'elleden.wsgi.application'

# Database
# Use SQLite for local development, PostgreSQL for production
if os.getenv('DATABASE_URL'):
    # Production: Use PostgreSQL via DATABASE_URL
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.config(default=os.getenv('DATABASE_URL'))
    }
else:
    # Development: Use SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Custom User Model
AUTH_USER_MODEL = 'accounts.User'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Africa/Nairobi'
USE_I18N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Media files
MEDIA_URL = 'media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Crispy Forms
CRISPY_ALLOWED_TEMPLATE_PACKS = 'bootstrap5'
CRISPY_TEMPLATE_PACK = 'bootstrap5'

# Login URLs
LOGIN_URL = 'accounts:login'
LOGIN_REDIRECT_URL = 'dashboard:customer_index'
LOGOUT_REDIRECT_URL = 'accounts:login'

# CSRF Settings - Add your Railway domain
CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1:8000',
    'http://localhost:8000',
] + [f'https://{host}' for host in ALLOWED_HOSTS if host and not host.startswith('.')]

# REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# JWT Settings
from datetime import timedelta
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=1),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
}

# CORS Settings
CORS_ALLOWED_ORIGINS = [
    'http://localhost:8000',
    'http://127.0.0.1:8000',
    'http://localhost:5500',
    'http://127.0.0.1:5500',
]
CORS_ALLOW_CREDENTIALS = True

# Email Settings (using console backend for testing)
# To print emails to server console instead of sending them
DEFAULT_FROM_EMAIL = 'Elleden Hotel <elledenhotelltd@gmail.com>'
# For Gmail SMTP (requires 2-Step Verification):
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER')
EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD')

# =============================================================================
# M-PESA DARAJA API SETTINGS
# =============================================================================
# Get credentials from Safaricom Developer Portal: https://developer.safaricom.co.ke
# 
# For sandbox (testing):
# - Create an app in the developer portal
# - Use sandbox credentials for testing
#
# For production:
# - Apply for production credentials (Go Live)
# - Set MPESA_ENVIRONMENT to 'production'
# =============================================================================

MPESA_ENVIRONMENT = os.getenv('MPESA_ENVIRONMENT', 'sandbox')  # 'sandbox' or 'production'
MPESA_CONSUMER_KEY = os.getenv('MPESA_CONSUMER_KEY', '')
MPESA_CONSUMER_SECRET = os.getenv('MPESA_CONSUMER_SECRET', '')
MPESA_SHORTCODE = os.getenv('MPESA_SHORTCODE', '174379')  # Sandbox default
MPESA_PASSKEY = os.getenv('MPESA_PASSKEY', 'bfb279f9aa9bdbcf158e97dd71a467cd2e0c893059b10f78e6b72ada1ed2c919')  # Sandbox default

# Callback URL - This must be a publicly accessible URL
# Use ngrok for local testing: ngrok http 8000
# Example: https://your-ngrok-url.ngrok.io/bookings/mpesa/callback/
MPESA_CALLBACK_URL = os.getenv('MPESA_CALLBACK_URL', 'https://your-domain.com/bookings/mpesa/callback/')

# =============================================================================
# AFRICA'S TALKING SMS SETTINGS
# =============================================================================
# Sign up at https://account.africastalking.com
# For testing: Use 'sandbox' as username and get your sandbox API key
# For production: Use your registered username and production API key
#
# Sender ID - Only for production. Apply for a shortcode/sender ID via the portal
# =============================================================================

AFRICASTALKING_USERNAME = os.getenv('AFRICASTALKING_USERNAME', 'sandbox')
AFRICASTALKING_API_KEY = os.getenv('AFRICASTALKING_API_KEY', '')
AFRICASTALKING_SENDER_ID = os.getenv('AFRICASTALKING_SENDER_ID', '')  # Optional: e.g., 'ELLEDEN'

