from .base import *

DEBUG = False

CORS_ORIGIN_ALLOW_ALL = True

INSTALLED_APPS = INSTALLED_LIBRARIES + INSTALLED_MODULES

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql_psycopg2',
#         'NAME': 'convocatoria',
#         'USER': 'postgres',
#         'PASSWORD': '123456',
#         'HOST': '127.0.0.1',
#         'PORT': '5432',
#     }
# }

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_remuneraciones',
        'USER': 'root',
        'PASSWORD': '',
        'HOST': '127.0.0.1',
        'PORT': '3306',
    }
}
