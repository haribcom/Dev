import dj_database_url

from .common import *

BASE_DIR_STATIC = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

DEBUG = False


# TODO: Add allowed host as per use in prod
ALLOWED_HOSTS = ['10.17.12.209', 'localhost', '127.0.0.1', '10.17.12.228', 'qamile.adityabirlalabs.com', '10.17.12.218',
                 'uatmile.adityabirlalabs.com', '10.17.12.170', 'mile.adityabirlalabs.com']

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
        'NAME': 'dna_ultratech_fare_dev_db',
        'OPTIONS': {
            'options': '-c search_path=dna_ultratech_fare_app'
        },
    },
    'ultra_tech': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dna_ultratech_fare_dev_db',
        'OPTIONS': {
            'options': '-c search_path=dna_ultratech_fare_dev'
        },
    },
    'chemicals': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'dna_ultratech_fare_dev_db',
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

STATICFILES_DIRS = (
    os.path.join(BASE_DIR_STATIC, 'static'),
)

STATIC_URL = '/api/static/'
STATIC_ROOT = os.path.join(BASE_DIR_STATIC, 'staticfiles')

MOCK = False