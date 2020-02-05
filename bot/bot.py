from telebot.types import Message, InlineKeyboardMarkup
from pymongo import MongoClient
import telebot

from threading import Thread
import os
import time
import datetime
import logging

from mongotools import *
import tools
import telegramtools
import timetools

from config import *


if "BOT_TOKEN" in list(os.environ.keys()):
    """
    If bot is started by heroku or innopolis vm
    """

    TOKEN = os.getenv('BOT_TOKEN')
    MONGO_URI = os.getenv('MONGODB_URI')
else:
    """
    If bot started by my computer
    """

    from TOKENS import TOKEN, MONGO_URI


# --------------------------
#        INITIAL SETUP
bot = telebot.TeleBot(TOKEN)
client = MongoClient(MONGO_URI)
db = client.heroku_2n5xgpck.roomBotDataBase
logger = tools.get_logger(__name__)
# --------------------------


class CheckTime(Thread):
    def run(self):
        while 1:
            # TODO: do check time
            timetools.check_time(bot, db, logger)
            time.sleep(60)


@bot.message_handler(commands=['start'])
def start_message(message: Message):
    """
    Start message + choose building.
    """

    if not chat_in_database(db, message.chat.id):
        createNew(db, message.chat.id)

    telegramtools.answer(bot, logger, message, START_MESSAGE)
    change_building(message)
    

@bot.message_handler(commands=['help'])
def start_message(message: Message):
    """
    Start message.
    """

    if not chat_in_database(db, message.chat.id):
        createNew(db, message.chat.id)

    telegramtools.answer(bot, logger, message, START_MESSAGE)

    

@bot.message_handler(commands=['changebuilding'])
def change_building(message: Message):
    telegramtools.answer(bot, logger, message, CHANGE_BUILDING_MESSAGE, reply_markup=telegramtools.generate_choose_day_button())


@bot.message_handler(commands=['schedule'])
def sendSchedule(message: Message):
    url = "https://hotel.university.innopolis.ru/assets/images/schedule.png"
    telegramtools.answer(bot, logger, message, url)


@bot.message_handler(commands=["nextcleaning"])
def sendNextCleaningDay(message: Message): 
    chat = get_chat(db, message.chat.id)
    building = int(chat['chosenbuilding'])

    if building is 0:
        telegramtools.answer(bot, logger, message, HAVE_NOT_BUILDING)
        return

    nextCleaning = timetools.get_next_cleaning_day(building)

    telegramtools.answer(bot, logger, message,
                     NEXT_DAY % (tools.ordinal(building),
                                 tools.ordinal(nextCleaning.day),
                                 timetools.getMonthName(nextCleaning)),
                     parse_mode='Markdown')


@bot.message_handler(commands=['addmember'])
def addmembers(message: Message):
    chat_id = message.chat.id
    if not chat_in_database(db, chat_id):
        startMessage(message)
        return

    aliases = message.text.split()[1:]
    if len(aliases) < 1:
        telegramtools.answer(bot, logger, message, ADDMEMBER_ERORR)
        return

    noticelist = extend_notice_list(db, chat_id, aliases)
    telegramtools.answer(bot, logger, message, SUCCESS_ADDMEMBER % '\n'.join(noticelist).replace('@', ''))


@bot.callback_query_handler(func=lambda call: call.data.startswith("__cb"))
def callback_query(call):
    """
    User has choosen building
    """

    if not chat_in_database(db, call.message.chat.id):
        start_message(call.message)
        return

    building = int(call.data[4:])
    update(db, call.message.chat.id, chosenbuilding=building, checknotice=True)
    logger.info(f"User {call.from_user.username} chose building {building}")
    telegramtools.change_message(bot, logger, call.message, 
                                 text=SUCCESS_BUILDING % tools.ordinal(building))

if __name__ == "__main__":
    bot_info = bot.get_me()
    logger.info(f"BOT STARTED: {bot_info.first_name} @{bot_info.username}")

    timeChecking = CheckTime()
    timeChecking.start()

    bot.infinity_polling()