from .base import *

DEBUG = True

SECRET_KEY = os.environ.get('SECRET_KEY')

ALLOWED_HOSTS = []

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'hasker',
        'USER': 'hasker',
        'PASSWORD': 'h@$keRApp1',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Pagination limits
QUESTIONS_PER_PAGE = 5
ANSWERS_PER_PAGE = 6
TRENDING_QUESTIONS = 7
