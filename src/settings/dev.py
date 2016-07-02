"""Development settings and globals."""

from os.path import join, normpath

from .common import *

# ######### DEBUG CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#debug
DEBUG = True
########## END DEBUG CONFIGURATION

########## TEMPLATE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#template-debug

TEMPLATES[0]['OPTIONS']['debug'] = DEBUG
########## END TEMPLATE CONFIGURATION

########## AUTH CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#secret-key
SECRET_KEY = r"1p)g!_znl4-_8gj%)1yfm7_##%3sj87y1u6b(zcr^fa11o5h2w"
########## END AUTH CONFIGURATION

########## DATABASE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#databases
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': normpath(join(DJANGO_ROOT, 'default.db')),
    'USER': '',
    'PASSWORD': '',
    'HOST': '',
    'PORT': '',
    # https://docs.djangoproject.com/en/dev/ref/databases/#database-is-locked-errors
    'OPTIONS': {
      'timeout': 20,
    }
  }
}

GRAPH_DB_URL = 'http://localhost:7474/db/data/'
GRAPH_DB_USERNAME = None
GRAPH_DB_PASSWORD = None
########## END DATABASE CONFIGURATION

########## CACHE CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#caches
CACHES = {
  'default': {
    'BACKEND': 'django_redis.cache.RedisCache',
    'LOCATION': 'localhost:6379',
    'OPTIONS': {
      'DB': 0,
    }
  }
}
########## END CACHE CONFIGURATION

########## LOGGING CONFIGURATION
# See: https://docs.djangoproject.com/en/dev/ref/settings/#logging

LOGGING['handlers']['console_handler'] = {
  'level': 'DEBUG',
  'class': 'rq.utils.ColorizingStreamHandler',
  # the diff between '()' and 'class' is that '()' could be a class OR some func. Refer to logging/config.py#695
  # http://stackoverflow.com/questions/9212228/using-custom-formatter-classes-with-pythons-logging-config-module
  'formatter': 'local_standard',
}

LOGGING['handlers']['file_handler'] = {
  'level': 'DEBUG',
  'class': 'logging.handlers.RotatingFileHandler',
  'filename': 'logs/app.log',
  'maxBytes': 1024 * 1024 * 5,  # 5 MB
  'backupCount': 10,
  'encoding': 'UTF-8',
  'formatter': 'local_standard'
}

LOGGING['handlers']['exception_handler'] = {
  'level': 'ERROR',
  'class': 'logging.handlers.RotatingFileHandler',
  'filename': 'logs/error.log',
  'maxBytes': 1024 * 1024 * 5,  # 5 MB
  'backupCount': 10,
  'encoding': 'UTF-8',
  'formatter': 'local_standard'
}

app_logger = {
  'handlers': ['console_handler', 'file_handler', 'exception_handler'],
  'level': 'DEBUG',
  'propagate': False
}

LOGGING['loggers'] = {
  '': app_logger,
  'django.request': app_logger,
  # django.request doesn't propagate by default https://docs.djangoproject.com/en/dev/topics/logging/#django-request
  'rq.worker': app_logger,
  # rq.worker is explicitly defined here because it's imported in common.py before logging is configured and is
  # subsequently disabled (disable_existing_loggers=True) so we need to provide an entry here to enable it.
}
########## END LOGGING CONFIGURATION

########### SOCIAL PROVIDER CONFIGURATION
TWITTER_APP_KEY = 'Twitter app key'
TWITTER_APP_SECRET = 'Twitter app secret'

LINKEDIN_API_KEY = 'LinkedIn api key'
LINKEDIN_API_SECRET = 'LinkedIn api secret'
LINKEDIN_USER_TOKEN = 'LinkedIn user token'
LINKEDIN_USER_SECRET = 'LinkedIn user secret'
LINKEDIN_REDIRECT_URI = 'http://localhost:8000/'

FULLCONTACT_API_KEY = 'FullContact api key'

REDDIT_SUBREDDIT_QUERY_LIMIT = 2
########## END SOCIAL PROVIDER CONFIGURATION

########### NLP CONFIGURATION
ALCHEMY_API_KEY = 'Alchemy Key'
########## END NLP CONFIGURATION

########### DRIVE CONFIGURATION
DRIVE_USERNAME = 'Drive user'
DRIVE_PASSWORD = 'Drive password'
DRIVE_ASSIGNMENT_SPREADSHEET_KEY = 'Drive Spreadsheet'
########## END DRIVE CONFIGURATION

########### EMAIL CONFIGURATION
SENDGRID_USERNAME = "Test_User"
SENDGRID_PASSWORD = "Password"
########## END EMAIL CONFIGURATION

########### EXTERNAL API CONFIGURATION
MASHAPE_API_KEY = "Mashape Api Key"
########## END EXTERNAL API CONFIGURATION

########### ANALYTICS CONFIGURATION
KEEN_PROJECT_ID = 'KEEN_PROJECT_ID'
KEEN_WRITE_KEY = 'KEEN_WRITE_KEY'
KEEN_READ_KEY = 'KEEN_READ_KEY'
########## END ANALYTICS CONFIGURATION
