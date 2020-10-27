"""
Django settings for odm2cvs project.
"""


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import json

DEBUG = True
TEMPLATE_DEBUG = False

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

data = {}
try:
    with open(os.path.join(BASE_DIR, 'settings', 'settings.json')) as data_file:
        data = json.load(data_file)
except IOError:
    print("You need to setup the settings data file (see instructions in base.py file.)")

try:
    SECRET_KEY = data["secret_key"]
except KeyError:
    print("The secret key is required in the settings.json file.")
    exit(1)

STATICFILES_DIRS = []

STATIC_ROOT = data['static_root']
STATIC_URL = '/static/'
SITE_URL = ''

RECAPTCHA_KEY = data["recaptcha_secret_key"] if "recaptcha_secret_key" in data else ""
RECAPTCHA_USER_KEY = data["recaptcha_user_key"] if "recaptcha_user_key" in data else ""
RECAPTCHA_VERIFY_URL = "https://www.google.com/recaptcha/api/siteverify"

ALLOWED_HOSTS = data["allowed_hosts"].split(" ") if "allowed_hosts" in data else []

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'tastypie',
    'cvservices',
    'cvinterface',
    'rdfserializer',
    'widget_tweaks',
]

MIDDLEWARE_CLASSES = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'wsgi.application'


# Databases
DATABASES = {}
for database in data['databases']:
    DATABASES[database['name']] = {
        'ENGINE': database['engine'],
        'NAME': database['schema'],
        'USER': database['user'] if 'user' in database else '',
        'PASSWORD': database['password'] if 'password' in database else '',
        'HOST': database['host'] if 'host' in database else '',
        'PORT': database['port'] if 'port' in database else '',
        'OPTIONS': database['options'] if 'options' in database else ''
    }

# Just for testing purposes
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': 'db.sqlite3',
#     },
#     'vocabularies': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': 'db.sqlite3',
#     }
# }

# Password validation
# https://docs.djangoproject.com/en/1.9/ref/settings/#auth-password-validators

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

USE_L10N = True

USE_TZ = True

TASTYPIE_DEFAULT_FORMATS = ['json']

API_LIMIT_PER_PAGE = 0

# SMTP server configuration

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_USE_TLS = True

EMAIL_HOST = 'smtp.gmail.com'

EMAIL_PORT = 587

EMAIL_HOST_USER = data['email_host_user'] if 'email_host_user' in data else ''

EMAIL_HOST_PASSWORD = data['email_host_password'] if 'email_host_password' in data else ''

EMAIL_SENDER = data['email_sender'] if 'email_sender' in data else ''
EMAIL_SENDER = EMAIL_SENDER[0] if isinstance(EMAIL_SENDER, tuple) else EMAIL_SENDER

EMAIL_RECIPIENTS = data['email_recipients'].split(" ") if 'email_recipients' in data else []
EMAIL_RECIPIENTS = EMAIL_RECIPIENTS[0] if isinstance(EMAIL_RECIPIENTS, tuple) else EMAIL_RECIPIENTS

DATABASE_ROUTERS = ['db_routers.ControlledVocabularyRouter']

# Logging configuration
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'level': os.getenv('DJANGO_LOG_LEVEL', 'INFO'),
        },
    },
}
