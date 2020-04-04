#!/usr/bin/env python
# -*- coding:utf-8 -*-

"""
Project: $Project$
Filename: $Filename$
Author: $Date$
Date: $Date$
Revision: $Revision$
Description: $Description$
"""

import pymysql

CONFIGS = {
    'redis': {
        'host': '127.0.0.1',
        'port': 6379,
        'password': '',
        'db': 1,
    },
    'mysql': {
        'host': 'test2.qianguisy.com',
        'port': 10097,
        'user': 'user',
        'password': 'Einiter',
        'database': 'lj_game',
        'maxConnections': 55,
        'minFreeConnections': 11,
    },
    'logger': {
        'version': 1,
        'formatters': {
            'format_def': {
                'class': 'logging.Formatter',
                'format': '[ %(asctime)s ] [%(levelname)s] class:%(name)s [file: %(filename)s: %(lineno)d ] %(message)s ',
                'datefmt': '%Y-%m-%d %H:%M:%S'
            }
        },
        'handlers': {
            'console': {
                'class': 'logging.StreamHandler',
                'level': 'INFO',
                'formatter': 'format_def'
            },
            'file': {
                'class': 'logging.handlers.RotatingFileHandler',
                'level': 'INFO',
                'formatter': 'format_def',
                'filename': 'log/server.log',
                'mode': 'a',
                'maxBytes': 10485760,
                'backupCount': 5
            }
        },
        'loggers': {
            'jobs': {
                'level': 'DEBUG',
                'propagate': 0,
                'handlers': [
                    'console', 'file'
                ]
            },
            'api': {
                'level': 'DEBUG',
                'propagate': 0,
                'handlers': [
                    'console'
                ]
            }
        }
    }
}
