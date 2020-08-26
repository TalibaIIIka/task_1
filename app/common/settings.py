import logging
import os
import sys


def get_logger(name='router'):
    if hasattr(get_logger, 'logger'):
        return get_logger.logger

    logger = logging.getLogger(name)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setLevel(os.environ.get('LOG_LEVEL', 'ERROR'))
    stream_formatter = logging.Formatter('%(asctime)s - %(filename)s:%(lineno)d - %(levelname)s - %(message)s')
    stream_handler.setFormatter(stream_formatter)
    logger.addHandler(stream_handler)

    get_logger.logger = logger

    return logger
