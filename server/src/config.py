#  -*- coding: utf-8 -*-

# NOTE: Do NOT commit this file!!!

DATABASE = {
    'drivername': 'postgresql',
    'host': 'archviz.humlab.umu.se',
    'username': 'humlab',
    'password': 'DeerCookie!!D',
    'port': '5432',
    'database': 'isleif_development'
}

import logging
def get_logger(level, name):
    logging.basicConfig(level=level)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger

def get_default_logger(name):
    return get_logger(logging.INFO, name)
