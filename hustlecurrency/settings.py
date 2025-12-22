"""
Django settings for hustlecurrency project.
"""

from pathlib import Path
import os
from decouple import config

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ===== VERCEL DETECTION =====
# Check if running on Vercel
ON_VERCEL = os.environ.get('VERCEL') == '1'

# Quick-start development settings
SECRET_KEY = 'uW9TJJvVoKL3lp06JqqsEsNY7SYpFRQHZdY_OwsPiniqisLrHrDmFWHR7PhDMDYmQGM'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if not ON_VERCEL else False  # Auto-disable debug on Vercel

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

# Database
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "neondb",
        "USER": "neondb_owner",
        "PASSWORD": "npg_6XOrDb0kjxLe",
        "HOST": "ep-cold-shadow-adhfbxim-pooler.c-2.us-east-1.aws.neon.tech",
        "PORT": "5432",
        "OPTIONS": {
            "sslmode": "require",
        },
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

# ===== STATIC FILES CONFIGURATION =====
if ON_VERCEL:
    # Vercel production settings
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Vercel expects 'staticfiles'
    
    # WhiteNoise configuration
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    
    # Disable media uploads (Vercel is read-only)
    MEDIA_URL = '/media/'
    MEDIA_ROOT = '/tmp/media'  # Vercel allows writes to /tmp
    
    # Create /tmp/media directory
    try:
        os.makedirs(MEDIA_ROOT, exist_ok=True)
    except:
        pass
        
else:
    # Local development settings
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')  # Same name for consistency
    STATICFILES_DIRS = [
        os.path.join(BASE_DIR, 'store', 'static'),  # Your app's static files
    ]
    
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
    
    # Media files for local
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Razorpay
RAZORPAY_KEY_ID = config('RAZORPAY_KEY_ID')
RAZORPAY_KEY_SECRET = config('RAZORPAY_KEY_SECRET')