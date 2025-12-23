"""
Django settings for hustlecurrency project.
"""

from pathlib import Path
import os
from decouple import config

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# ===== VERCEL DETECTION =====
ON_VERCEL = os.environ.get('VERCEL') == '1'

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config('SECRET_KEY', 'uW9TJJvVoKL3lp06JqqsEsNY7SYpFRQHZdY_OwsPiniqisLrHrDmFWHR7PhDMDYmQGM')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if not ON_VERCEL else False  # Auto-disable on Vercel

ALLOWED_HOSTS = ['.vercel.app', 'localhost', '127.0.0.1']

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'store'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
]

ROOT_URLCONF = 'hustlecurrency.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'hustlecurrency.wsgi.application'

# ===== DATABASE CONFIGURATION =====
# Use environment variables for security!
if ON_VERCEL:
    # Production database (Neon)
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": config('NEON_DB_NAME', 'neondb'),
            "USER": config('NEON_DB_USER', 'neondb_owner'),
            "PASSWORD": config('NEON_DB_PASSWORD', 'npg_6XOrDb0kjxLe'),
            "HOST": config('NEON_DB_HOST', 'ep-cold-shadow-adhfbxim-pooler.c-2.us-east-1.aws.neon.tech'),
            "PORT": "5432",
            "OPTIONS": {
                "sslmode": "require",
            },
        }
    }
else:
    # Local development - SQLite
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# ===== FILE STORAGE CONFIGURATION =====
if ON_VERCEL:
    # Production - Use Vercel Blob Storage
    try:
        DEFAULT_FILE_STORAGE = 'hustlecurrency.vercel_blob_storage.VercelBlobStorage'
    except ImportError:
        # Fallback if storage backend not created yet
        DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
        MEDIA_ROOT = '/tmp/media'  # Vercel allows writes to /tmp
    
    BLOB_READ_WRITE_TOKEN = os.environ.get('BLOB_READ_WRITE_TOKEN', 'vercel_blob_rw_iZtShuv0oL15yu1U_JUdgKehSLY6OPD3uSn3sRhBzWxuf7B')
    MEDIA_URL = 'https://hustler-currency-website.vercel.app/'
    
else:
    # Local development - Use local file system
    DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# ===== STATIC FILES CONFIGURATION =====
STATIC_URL = '/static/'

if ON_VERCEL:
    # Vercel production
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Vercel expects this
    STATICFILES_DIRS = []
else:
    # Local development
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
    STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Razorpay
RAZORPAY_KEY_ID = config('RAZORPAY_KEY_ID')
RAZORPAY_KEY_SECRET = config('RAZORPAY_KEY_SECRET')