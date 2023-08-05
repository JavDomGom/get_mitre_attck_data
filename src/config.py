"""
get_mitre_attck_data
@authors: JavDomGom
"""

import os

TRACE_LEVEL = os.getenv('TRACE_LEVEL', 'INFO')
LOG_PATH = os.getenv('LOG_PATH', 'log')
LOG_MAX_MEGABYTES = int(os.getenv('LOG_MAX_BYTES', '5'))
LOG_MAX_FILES = int(os.getenv('LOG_MAX_FILES', '3'))
LOG_FORMATTER = '{"time":"%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}'
