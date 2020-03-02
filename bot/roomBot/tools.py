import logging 
import sys
import math
from enum import Enum

from . import mongotools
from . import config
from . import timetools
from . import telegramtools


class States():
    """
    A simple state machine
    """
    STATE_DEFAULT = 0
    STATE_WAIT_FOR_ADD = 1


def in_private_message(message) -> bool:
    return message.chat.id == message.from_user.id


def get_logger(name=__name__):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    logger_handler = logging.FileHandler(config.PATH_TO_BOT_LOG_FILE)
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


def next_cleaning_day(chat_id) -> str:
    """
    Returns the next cleaning day for user/chat with such chat_id
    """
    
    if not mongotools.chat_in_database(chat_id):
        mongotools.createNew(chat_id)
    
    chat = mongotools.get_chat(chat_id)


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

    if error:
        if isinstance(message, Exception):
            logger.exception(message)
        else:
            logger.error(message)
    else:
        # Delete all emoji from the message
        message = message.encode('ascii', 'ignore').decode('ascii')
        logger.info(message)
    
    print(message)

def proccess_change_menu(chat_id: str, query: str):
    """
    handle query from buttons, returns new buttons
    """

    _, command, name = query.split('|')

    if command == config.INCREASE:
        if mongotools.change_amount_of_items(chat_id, name, 1):
            pass
        else:
            raise NameError
    elif command == config.DECREASE:
        if mongotools.change_amount_of_items(chat_id, name, -1):
            pass
        else:
            raise NameError
    
    
    return telegramtools.generate_buy_list(mongotools.get_safe(chat_id, 'buylist'))