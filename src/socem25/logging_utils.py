# src/socem25/logging_utils.py

import logging

def setup_logger():
    logger = logging.getLogger("socem25")
    logger.setLevel(logging.DEBUG)
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(levelname)s] %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger
