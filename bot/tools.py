import logging 
import sys
import math

def get_logger(name=__name__):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
 
    logger_handler = logging.StreamHandler(sys.stdout)
    logger_handler.setLevel(logging.INFO)
 
    logger_formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s \t| %(message)s')
 
    logger_handler.setFormatter(logger_formatter)
 
    logger.addHandler(logger_handler)
    return logger


def ordinal(n):
    """
    Returns the ordinal number of the number
    1 -> 1st
    3 -> 3rd
    5 -> 5th
    """
    return "%d%s" % (n, "tsnrhtdd"[(math.floor(n / 10) % 10 != 1) * (n % 10 < 4) * n % 10::4])

