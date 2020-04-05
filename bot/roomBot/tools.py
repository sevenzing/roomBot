import logging 
import sys
import math
from enum import Enum
from telebot.types import CallbackQuery

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


def cut_text(text):
    return text if len(text) < 20 else text[:20] + "..."


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


def process_change_menu(bot, call: CallbackQuery):
    """
    handle query from buttons, returns new buttons
    """
    chat_id = call.message.chat.id
    _, command, name = call.data.split('|')

    if command == config.INCREASE:
        mongotools.change_amount_of_items(chat_id, name, 1)
    
    elif command == config.DECREASE:
        mongotools.change_amount_of_items(chat_id, name, -1)
        
    elif command == config.CLEAR:
        mongotools.update(chat_id, buylist={})
        return telegramtools.change_message(bot, call.message, config.LIST_WAS_DELETED, 
                                     reply_markup=telegramtools.generate_empty_buttons())
    

    elif command == config.EXIT:
        return telegramtools.delete_message(bot, call.message)


    telegramtools.change_message(bot, call.message,
                                 reply_markup=telegramtools.generate_buy_list(mongotools.get_safe(chat_id, 'buylist')))

def change_notice_state(chat_id):
    chat = mongotools.get_chat(chat_id)
    
    if chat['checknotice']:
        mongotools.update(chat_id, checknotice=False)
        return config.NOTICE_OFF
    else:
        mongotools.update(chat_id, checknotice=True)
        return config.NOTICE_ON

