"""Development settings and globals."""

# noinspection PyUnresolvedReferences
from .dev import *

LOGGING['loggers']['factory'] = dict(app_logger, **{'level': 'INFO'})
