from pathlib import Path
import os
from dotenv import load_dotenv
load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIRS = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR =os.path.join(BASE_DIRS,'templates')
STATIC_DIR=os.path.join(BASE_DIRS,'static')


SECRET_KEY = os.getenv('SECRET_KEY')
DEBUG = os.getenv('DEBUG')

ALLOWED_HOSTS = ["*"]


INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'home'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'timecapsule.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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

WSGI_APPLICATION = 'timecapsule.wsgi.application'


DATABASES = {
    'default': {
       'ENGINE': 'django.db.backends.sqlite3',
      'NAME': BASE_DIR / 'db.sqlite3',
  }
}


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


LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

STATIC_URL = '/static/'
MEDIA_URL='/media/'
STATICFILES_DIRS = os.path.join(BASE_DIR,'static'),
STATIC_ROOT  = os.path.join(BASE_DIR,'staticfiles_build','static')
MEDIA_ROOT=os.path.join(BASE_DIR,'media')


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



EMAIL_BACKEND =  os.getenv('EMAIL_BACKEND')
EMAIL_HOST_USER =  os.getenv('EMAIL_HOST_USER')
EMAIL_HOST =  os.getenv('EMAIL_HOST')
EMAIL_PORT=  os.getenv('EMAIL_PORT')
EMAIL_USE_TLS =  os.getenv('EMAIL_USE_TLS')
EMAIL_HOST_PASSWORD =  os.getenv('EMAIL_HOST_PASSWORD')


SCHEDULER_DEFAULT = True



TWILIO_ACCOUNT_SID =  os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN =  os.getenv('TWILIO_AUTH_TOKEN')


AUTH_USER_MODEL = 'home.User'
