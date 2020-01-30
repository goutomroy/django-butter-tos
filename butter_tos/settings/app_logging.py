import logging.config
import os
import environ
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# sentry settings
BASE_DIR = environ.Path(__file__) - 3
env = environ.Env()
environ.Env.read_env(env_file=os.path.join(BASE_DIR, 'app.env'))
sentry_sdk.init(
    dsn=env.str('SENTRY_DNS'),
    integrations=[DjangoIntegration()],

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

# Disable Django's logging setup
LOGGING_CONFIG = None
LOG_LEVEL = os.environ.get('LOGLEVEL', 'info').upper()
logging.config.dictConfig(
    {
        'version': 1,
        'disable_existing_loggers': False,
        'filters': {
            'require_debug_false': {
                '()': 'django.utils.log.RequireDebugFalse',
            },
            'require_debug_true': {
                '()': 'django.utils.log.RequireDebugTrue',
            },
        },
        'formatters': {
            'default': {
                # exact format is not important, this is the minimum information
                'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s',
            },
            'django.server': {
                '()': 'django.utils.log.ServerFormatter',
                'format': '[{server_time}] {message}',
                'style': '{',
            }
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'filters': ['require_debug_true'],
                'class': 'logging.StreamHandler',
            },
            'sentry': {
                'level': 'WARNING',
                'filters': ['require_debug_false'],
                'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            },
        },
        'loggers': {
            # default for all undefined Python modules
            '': {
                'level': 'WARNING',
                'handlers': ['console', 'sentry'],
                'propagate': False,
            },
            # Our application code
            'butter_tos.apps': {
                'level': 'INFO',
                'handlers': ['console', 'sentry'],
                # Avoid double logging because of root logger
                'propagate': False,
            },
            # root logger for project
            'django': {
                'handlers': ['console'],
                'level': 'INFO',
            },
        }
    }
)
