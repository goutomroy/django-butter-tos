import logging.config
import os
import environ
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# sentry settings
env = environ.Env()
environ.Env.read_env(env_file=os.path.join((environ.Path(__file__) - 3), 'app.env'))
DEBUG = env.bool('DEBUG', default=False)

if DEBUG is False:
    sentry_sdk.init(
        dsn=env.str('SENTRY_DNS'),
        integrations=[DjangoIntegration()],
        # If you wish to associate users to errors (assuming you are using
        # django.contrib.auth) you may enable sending PII data.
        send_default_pii=True
    )

# Disable Django's logging setup
LOGGING_CONFIG = None
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
                'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
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
            'django.server': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'django.server',
            },
            'mail_admins': {
                'level': 'ERROR',
                'filters': ['require_debug_false'],
                'class': 'django.utils.log.AdminEmailHandler'
            }
        },
        'loggers': {
            # Our application code
            'apps': {
                'level': 'INFO',
                'handlers': ['console', 'sentry'],
                'propagate': False,
            },
            # default for all undefined Python modules
            '': {
                'level': 'WARNING',
                'handlers': ['console', 'sentry'],
                'propagate': False,
            },

            # root logger for project
            'django': {
                'handlers': ['console', 'mail_admins'],
                'level': 'INFO',
            },
            'django.server': {
                'handlers': ['django.server'],
                'level': 'INFO',
                'propagate': False,
            }
        }
    }
)
