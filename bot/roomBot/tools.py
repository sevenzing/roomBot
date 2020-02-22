import logging 
import sys
import math

from . import mongotools
from . import config
from . import timetools


def in_private_message(message) -> bool:
    return message.chat.id == message.from_user.id


def get_logger(name=__name__):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
 
    #logger_handler = logging.StreamHandler(sys.stdout)
    logger_handler = logging.FileHandler("roomBot.log")
    logger_handler.setLevel(logging.INFO)
 
    logger_formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s \t| %(message)s')
 
    logger_handler.setFormatter(logger_formatter)
 
    logger.addHandler(logger_handler)
    return logger


def ordinal(n: int) -> str:
    """
    Returns the ordinal number of the number
    1 -> 1st
    3 -> 3rd
    5 -> 5th
    """
    return "%d%s" % (n, "tsnrhtdd"[(math.floor(n / 10) % 10 != 1) * (n % 10 < 4) * n % 10::4])


def next_cleaning_day(db, chat_id):
    """
    Returns the next cleaning day from user/chat with such chat_id
    """
    
    if not mongotools.chat_in_database(db, chat_id):
        mongotools.createNew(db, chat_id)
    
    chat = mongotools.get_chat(db, chat_id)


    building = int(chat['chosenbuilding'])

    if building == 0:
        return config.HAVE_NOT_BUILDING

    nextCleaningDate = timetools.get_next_cleaning_day(building)
    return config.NEXT_DAY % (ordinal(building),
                       timetools.daysLeft(nextCleaningDate),
                       ordinal(nextCleaningDate.day),
                       timetools.getMonthName(nextCleaningDate))


logger = get_logger(__name__)


def log(message, error=False):
    """
    Write message in log file and console 
    """

    # Delete all emoji from the message
    message = message.encode('ascii', 'ignore').decode('ascii')
    if error:
        if isinstance(message, Exception):
            logger.exception(message)
        else:
            logger.error(message)
    else:
        logger.info(message)
    
    print(message)

