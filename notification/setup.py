import telebot
import logging
from roomBot import config
from roomBot.database import db


def get_logger(name, path):
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    logger_handler = logging.FileHandler(path)
    logger_handler.setLevel(logging.INFO)
 
    logger_formatter = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s \t| %(message)s')
 
    logger_handler.setFormatter(logger_formatter)
 
    logger.addHandler(logger_handler)
    return logger



bot = telebot.TeleBot(config.BOT_TOKEN)

logger = get_logger(__name__, config.PATH_TO_NOTIFICATION_LOG_FILE)