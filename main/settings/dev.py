from .base import *
import os

DEBUG = os.environ.setdefault('DEBUG', 'False')

CORS_ORIGIN_ALLOW_ALL = True

INSTALLED_APPS = INSTALLED_LIBRARIES + INSTALLED_MODULES
SESSION_COOKIE_AGE = 60 * 60 *2
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'haberes_2024',
        'USER': 'root',
        'PASSWORD': 'Administrador@123',
        'HOST': 'mysql',
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    },
    'haberes_2025': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'haberes_2025',
        'USER': 'root',
        'PASSWORD': 'Administrador@123',
        'HOST': 'mysql',
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    },
    'haberes_2024': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'haberes_2024',
        'USER': 'root',
        'PASSWORD': 'Administrador@123',
        'HOST': 'mysql',
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    },
    'haberes_2023': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'haberes_2023',
        'USER': 'root',
        'PASSWORD': 'Administrador@123',
        'HOST': 'mysql',
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    },
    'haberes_2022': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'haberes_2022',
        'USER': 'root',
        'PASSWORD': 'Administrador@123',
        'HOST': 'mysql',
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    },
    'haberes_2021': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'haberes_2021',
        'USER': 'root',
        'PASSWORD': 'Administrador@123',
        'HOST': 'mysql',
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    },
    'haberes_2020': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'haberes_2020',
        'USER': 'root',
        'PASSWORD': 'Administrador@123',
        'HOST': 'mysql',
        'PORT': '3306',
    },
    'haberes_2019': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'haberes_2019',
        'USER': 'root',
        'PASSWORD': 'Administrador@123',
        'HOST': 'mysql',
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    },
    'haberes_2018': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'haberes_2018',
        'USER': 'root',
        'PASSWORD': 'Administrador@123',
        'HOST': 'mysql',
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    },
    'haberes_2017': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'haberes_2017',
        'USER': 'root',
        'PASSWORD': 'Administrador@123',
        'HOST': 'mysql',
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    },
    'haberes_2016': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'haberes_2016',
        'USER': 'root',
        'PASSWORD': 'Administrador@123',
        'HOST': 'mysql',
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    },
    'haberes_2015': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'haberes_2015',
        'USER': 'root',
        'PASSWORD': 'Administrador@123',
        'HOST': 'mysql',
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    },

    'haberes_2014': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'haberes_2014',
        'USER': 'root',
        'PASSWORD': 'Administrador@123',
        'HOST': 'mysql',
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    },
    'haberes_2013': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'haberes_2013',
        'USER': 'root',
        'PASSWORD': 'Administrador@123',
        'HOST': 'mysql',
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    },
}
