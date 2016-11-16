
DATABASE = {
    'drivername': 'postgresql',
    'username': 'your-username',
    'host': 'your-server-name',
    'password': 'your-password',
    'port': '5432',
    'database': 'your-database-name'
}

import logging
def get_logger(level, name):
    logging.basicConfig(level=level)
    logger = logging.getLogger(name)
    logger.setLevel(level)
    return logger

def get_default_logger(name):
    return get_logger(logging.INFO, name)
