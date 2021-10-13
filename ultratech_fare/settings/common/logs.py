# log files are created in current working directory
import os

LOG_DIR = os.environ.get('LOG_DIR', '')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(filename)s %(lineno)d %(message)s",
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        },
    },
    'handlers': {
        'file': {
            'level': os.environ.get('LOG_LEVEL', 'INFO'),
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'midnight',
            'backupCount': 30,
            'filename': os.path.join(LOG_DIR, './application.log'),
            'formatter': 'verbose',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'filters': ['require_debug_true'],
            'formatter': 'verbose'
        },
        'sql': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'backupCount': 30,
            'filename': os.path.join(LOG_DIR, './queries.log'),
            'filters': ['require_debug_true'],
            'formatter': 'verbose',
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
        'acn_historical_data': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'acn_forecast_data': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'core': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'acn_scenario': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': True,
        },

        'django.db.backends': {
            'level': 'DEBUG',
            'handlers': ['sql'],
            'propagate': False,
        },
    }
}
