"""
Django settings for core project.

Generated by 'django-admin startproject' using Django 3.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
from decouple import config
from datetime import timedelta
from corsheaders.defaults import default_headers
from .common import token_time

# Custom user model
AUTH_USER_MODEL = 'account.Account'

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config("SECRET_KEY", default="12345678")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config("DEBUG", default="TRUE", cast=bool)

ALLOWED_HOSTS = []

# Prevent redirect when user does not end an endpoint with a slash. May cause data to not be sent to the redirected url when this field is set to False
APPEND_SLASH = False

# Application definition
INSTALLED_APPS = [
    "rest_framework",
    "rest_framework_simplejwt",
    "corsheaders",
    # "drf_yasg",
    "drf_spectacular",
    "api",
    "account",
    "category",
    "departments",
    "doctors",

    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS
# CORS_ALLOW_ALL_ORIGINS = True # If this is used then `CORS_ORIGIN_WHITELIST` will not have any effect
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://tombra4ril.com:3000",
]
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_REGEX_WHITELIST = [
    'http://localhost:3000',
]
CORS_ALLOW_HEADERS = list(default_headers) + [
    'credentials',
    "withcredentials",
    "access-control-allow-credentials",
    "Access-Control-Expose-Headers",
    "access-control-allow-origin",
]
CORS_EXPOSE_HEADERS = [
    "Set-Cookie",
    "credentials",
    "access-control-allow-crendentials",
    "access-control-allow-origin",
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

# Rest framework settings
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    "DEFAULT_PERMISSION_CLASSES": (
        "rest_framework.permissions.IsAuthenticated",
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

# Drf-spectacular documentation
SPECTACULAR_SETTINGS = {
    'TITLE': 'Hospital Management System API',
    'DESCRIPTION': 'This api gives a summary of all the apis and how to use them.',
    'VERSION': f"{config('VERSION', default='1.0.0')}.{config('VERSION_MAJOR', default='0')}.{config('VERSION_MINOR', default='0')}",
    # OTHER SETTINGS
}

# Swagger documentation
# SWAGGER_SETTINGS = {
#     'SECURITY_DEFINITIONS': {
#         'Auth token eg [Bearer (JWT)]': {
#             'type': 'apiKey',
#             "name": "Authorization",
#             "in": "header",
#         }
#     },
# }

# Simple jwt settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': token_time(
        config(
            "TOKEN_EXPIRES_IN_TYPE", 
            default="minutes"
        ), 
        type="TOKEN"
    ),
    'REFRESH_TOKEN_LIFETIME': token_time(
        config(
            "REFRESH_EXPIRES_IN_TYPE", 
            default="hours"
        ), 
        type="REFRESH"
    ),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'uuid',
    'USER_ID_CLAIM': 'uuid',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}

# Email configuration
EMAIL_HOST = config("EMAIL_HOST", default="localhost")
EMAIL_PORT = config("EMAIL_PORT", default="8001")
EMAIL_HOST_USER = config("EMAIL_HOST_USER", default="webmaster4tombra@gmail.com")
EMAIL_HOST_PASSWORD = config("EMAIL_HOST_PASSWORD", default="asdf;lkj")
EMAIL_USE_TLS = config("EMAIL_USE_TLS", default="False", cast=bool)
# EMAIL_USE_SSL = config("EMAIL_USE_SSL", default="False", cast=bool)

WSGI_APPLICATION = 'core.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': config('DB_ENGINE', default="django.db.backends.sqlite3"),
        "NAME": config("DB_NAME", default=BASE_DIR / "db.sqlite3"),
        "USER": config("DB_USER", default="postgres"),
        "PASSWORD": config("DB_PASS", default="12345678"),
        "HOST": config("DB_HOST", default="localhost"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

STATIC_URL = '/static/'
