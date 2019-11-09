from .base import *

DEBUG = False

ALLOWED_HOSTS = ['*']

EMAIL_BACKEND = 'django.core.mail.backends.filebased.EmailBackend'
EMAIL_FILE_PATH = '/tmp/haskermail'

QUESTIONS_PER_PAGE = 20
ANSWERS_PER_PAGE = 30
TRENDING_QUESTIONS = 20
