from .base import *
import os

DEBUG = os.environ.setdefault('DEBUG', 'False')

ALLOWED_HOSTS = ['*']
CORS_ORIGIN_ALLOW_ALL = True

INSTALLED_APPS = INSTALLED_LIBRARIES + INSTALLED_MODULES
SESSION_COOKIE_AGE = 60 * 60 *2
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
DATABASE_HOST = os.environ.setdefault('DB_HOST', 'host')
DATABASE_USERNAME = os.environ.setdefault('DB_USERNAME', 'user')
DATABASE_PASSWORD = os.environ.setdefault('DB_PASSWORD', 'password')
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'haberes_2015',
        'USER': DATABASE_USERNAME,
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': DATABASE_HOST,
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    },
    'haberes_2025': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'haberes_2025',
        'USER': DATABASE_USERNAME,
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': DATABASE_HOST,
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    },
    'haberes_2024': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'haberes_2024',
        'USER': DATABASE_USERNAME,
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': DATABASE_HOST,
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    },
    'haberes_2023': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'haberes_2023',
        'USER': DATABASE_USERNAME,
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': DATABASE_HOST,
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    },
    'haberes_2022': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'haberes_2022',
        'USER': DATABASE_USERNAME,
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': DATABASE_HOST,
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    },
    'haberes_2021': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'haberes_2021',
        'USER': DATABASE_USERNAME,
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': DATABASE_HOST,
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    },
    'haberes_2020': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'haberes_2020',
        'USER': DATABASE_USERNAME,
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': DATABASE_HOST,
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    },
    'haberes_2019': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'haberes_2019',
        'USER': DATABASE_USERNAME,
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': DATABASE_HOST,
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    },
    'haberes_2018': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'haberes_2018',
        'USER': DATABASE_USERNAME,
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': DATABASE_HOST,
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    },
    'haberes_2017': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'haberes_2017',
        'USER': DATABASE_USERNAME,
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': DATABASE_HOST,
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    },
    'haberes_2016': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'haberes_2016',
        'USER': DATABASE_USERNAME,
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': DATABASE_HOST,
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    },
    'haberes_2015': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'haberes_2015',
        'USER': DATABASE_USERNAME,
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': DATABASE_HOST,
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    },

    'haberes_2014': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'haberes_2014',
        'USER': DATABASE_USERNAME,
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': DATABASE_HOST,
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    },
    'haberes_2013': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'haberes_2013',
        'USER': DATABASE_USERNAME,
        'PASSWORD': DATABASE_PASSWORD,
        'HOST': DATABASE_HOST,
        'PORT': '3306',
        'OPTIONS': {
            'sql_mode': 'traditional',
        }
    },
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        "require_debug_false": {
            "()": "django.utils.log.RequireDebugFalse"
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue',
        },
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)classification_dropdown %(asctime)classification_dropdown %(module)classification_dropdown %(process)d %(thread)d %(message)classification_dropdown'
        },
        'app': {
            'format': "[%(asctime)classification_dropdown] [%(levelname)classification_dropdown] [%(name)classification_dropdown:%(lineno)classification_dropdown] [%(path)classification_dropdown] [%(ip)classification_dropdown] [%(user)classification_dropdown] %(message)classification_dropdown",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
        'tracing': {
            'format': "[%(asctime)classification_dropdown] [%(levelname)classification_dropdown] [%(name)classification_dropdown:%(lineno)classification_dropdown] [%(path)classification_dropdown] [%(remote_host)classification_dropdown] [%(server_name)classification_dropdown] [%(language)classification_dropdown] [%(user_agent)classification_dropdown] [%(http_host)classification_dropdown] [%(ip)classification_dropdown] [%(user)classification_dropdown] %(message)classification_dropdown",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'filters': ['require_debug_false']
        },
        'sentry_warning': {
            'level': 'WARNING',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'filters': ['require_debug_false']
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
            'filters': ['require_debug_true']
        }

    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'access.blacklist': {
            'level': 'WARNING',
            'handlers': ['sentry_warning'],
            'propagate': False,
        },
    },
    'root': {
        'level': 'WARNING',
        'handlers': ['console', 'sentry', ]
    },
}
