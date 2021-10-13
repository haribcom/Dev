import os

import dj_database_url

from .common import *

DEBUG = True
ALLOWED_HOSTS = ['*']

STATIC_HOST = os.environ.get('DJANGO_STATIC_HOST', '')

# STATIC_ROOT = os.path.join(BASE_DIR, './static')

STATIC_ROOT = 'staticfiles'

STATIC_URL = '/static/'

DATABASE_ROUTERS = ['ultratech_fare.settings.routers.UserRouter',
                    'ultratech_fare.settings.routers.UltraTechRouter',
                    'ultratech_fare.settings.routers.ChemicalsRouter']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    },
    'admin': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'fare',
        'OPTIONS': {
            'options': '-c search_path=dna_ultratech_fare_app'
        },
    },
    'ultra_tech': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'fare',
        'OPTIONS': {
            'options': '-c search_path=dna_ultratech_fare_dev'
        },
    },
    'chemicals': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'fare',
        'OPTIONS': {
            'options': '-c search_path=dna_chemicals_fare_dev'
        },
    }
}

# Use the database configuration defined in environment variable DATABASE_URL

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['admin'].update(db_from_env)
DATABASES['ultra_tech'].update(db_from_env)
DATABASES['chemicals'].update(db_from_env)

MOCK = False
