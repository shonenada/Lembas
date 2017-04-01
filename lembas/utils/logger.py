# -*- coding: utf-8 -*-

from __future__ import absolute_import

import os

from envcfg.raw import lembas


LOGGING_CONFIG = {
    'version': 1,
    'formatters': {
        'console_format': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
        'file_format': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'DEBUG',
            'formatter': 'console_format',
            'stream': 'ext://sys.stdout',
        },
        'file': {
            'class': 'logging.FileHandler',
            'level': 'WARNING',
            'formatter': 'file_format',
            'filename': '/tmp/lembas.log',
        },
    },
    'loggers': {
        'console': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'file': {
            'level': 'WARNING',
            'handlers': ['file'],
            'propagate': False,
        },
    },
    'root': {
        'level': 'DEBUG',
        'handlers': ['console', 'file'],
    },
}


def setup_logger(app):
    if not app.debug and not app.config['TESTING']:
        import logging.config
        logging.config.dictConfig(LOGGING_CONFIG)
    else:
        import logging
        logging.basicConfig(level='DEBUG')


class LogWriter(object):

    def __init__(self, filename):
        self.log_path = os.path.join(lembas.ACCESS_LOG_PATH, filename)

    def log(self, message, *args):
        with open(self.log_path, 'a+') as out:
            out.write('%s\n' % (message % args))
