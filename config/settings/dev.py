from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []

# Email settings
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Pagination limits
QUESTIONS_PER_PAGE = 5
ANSWERS_PER_PAGE = 6
TRENDING_QUESTIONS = 7
