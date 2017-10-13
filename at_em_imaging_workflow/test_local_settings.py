import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_ROOT = BASE_DIR

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detailed': {
            'class': 'logging.Formatter',
            'format': '%(asctime)s %(name)-15s %(levelname)-8s %(processName)-10s %(message)s'
        }
    },    
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(PROJECT_ROOT, 'test_debug.log'),
            'formatter': 'detailed'
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'test_output': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'workflow_engine': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'celery': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'celery.task': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        }        
    }
}

