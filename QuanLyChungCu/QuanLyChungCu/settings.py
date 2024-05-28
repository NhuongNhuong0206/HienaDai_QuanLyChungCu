"""
Django settings for QuanLyChungCu project.

Generated by 'django-admin startproject' using Django 5.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.0/ref/settings/
"""

import pymysql

pymysql.version_info = (1, 4, 3, "final", 0)
pymysql.install_as_MySQLdb()

AUTH_USER_MODEL = 'QlChungCu.User'

import cloudinary

cloudinary.config(
    cloud_name = "hiendai",
    api_key = "358894412554338",
    api_secret = "achoo--NvftyIBf-7AUzdDgLMZc", # Click 'View Credentials' below to copy your API secret
    # api_proxy = "http://proxy.server:3128"
)

import cloudinary.uploader
import cloudinary.api
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

MEDIA_ROOT = '%s/QlChungCu/static/' % BASE_DIR

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-e00(c)y-8jz=z--*5^wgx+j%_85jro1+g(3!$abw*il3wrmx@d'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# ALLOWED_HOSTS = ['6f4c-171-243-48-141.ngrok-free.app']
ALLOWED_HOSTS = []
CSRF_TRUSTED_ORIGINS = ['http://127.0.0.1:8000', 'https://6f4c-171-243-48-141.ngrok-free.app']
# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'QlChungCu.apps.QlchungcuConfig',
    'rest_framework',
    'drf_yasg',
    'oauth2_provider',
    'ckeditor',
    'ckeditor_uploader',
    'corsheaders',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

ROOT_URLCONF = 'QuanLyChungCu.urls'
CORS_ORIGIN_ALLOW_ALL = True
CORS_ORIGIN_WHITELIST = (
    'http://localhost:3000',  # Địa chỉ IP hoặc tên miền của ứng dụng React Native
    'http://192.168.1.222:8081:delete',
    'exp://192.168.1.222:8081:delete'# Ví dụ: địa chỉ IP của Metro bundler
    # Thêm các địa chỉ IP hoặc tên miền khác nếu cần
)



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

CKEDITOR_UPLOAD_PATH = "ckeditors/images"

WSGI_APPLICATION = 'QuanLyChungCu.wsgi.application'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.contrib.rest_framework.OAuth2Authentication',
    )
}

# Database
# https://docs.djangoproject.com/en/5.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'QLCDdb',
        'USER': 'root',
        'PASSWORD': 'Admin@123',
        'HOST': ''  # mặc định localhost
    }
}

# Password validation
# https://docs.djangoproject.com/en/5.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/5.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.0/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/5.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
CLIENT_ID = 'JtzDKPoyGsBUuOUYAeiGOO3tZIYTrI1yOVVeXT0i'
CLIENT_SECRET = 'KEyUJlDBu5qBIxvfDraodFSlLTt3RtokHR1LGZalCupw8YZK3cQYK7NFEH9oW1Qs9cZ4Rxbxj5DXwZvZ8lUiSGXGhiAUAMSIPwuZWIcXTm4TtcA0J9Nii64X8N5sOrkI'
