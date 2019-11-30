import pymongo
import telebot
from telebot.types import Message
import os
from pymongo import MongoClient
import src
from pythoncalendar import create_calendar, process_calendar_selection, checkTime
from MESSAGES import *
from mongotools import *
from threading import Thread
import time
import calendar

class CheckTime(Thread):
    def run(self):
        while 1:
            print("check time start!")
            checkTime(db, bot)
            time.sleep(60)

if "HEROKU" in list(os.environ.keys()):
    """
    If bot is started by heroku
    """

    TOKEN = os.getenv('BOT_TOKEN')
    MONGO_URI = os.getenv('MONGODB_URI')
else:
    """
    If bot started by my computer
    """

    from TOKENS import TOKEN, MONGO_URI

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['schedule'])
def sendSchedule(message: Message):
    chat_id = message.chat.id
    if not room_in_database(db, chat_id):
        startMessage(message)
        return

    url = "https://hotel.university.innopolis.ru/assets/images/schedule.png"
    name = src.saveScheduleImage(url)
    bot.send_photo(chat_id, src.getScheduleImage(name))


@bot.message_handler(commands=['start'])
def startMessage(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, START_MESSAGE)

    if not room_in_database(db, chat_id):
        createNew(db, chat_id)

@bot.message_handler(commands=['addmember'])
def addmembers(message: Message):
    chat_id = message.chat.id
    if not room_in_database(db, chat_id):
        startMessage(message)
        return

    aliases = message.text.split()
    if len(aliases) < 2:
        bot.send_message(chat_id, ADDMEMBER_ERORR)
        return

    chat = get_chat(db, chat_id)
    noticelist = eval(chat['noticelist'])
    noticelist.extend(aliases[1:])
    noticelist = list(set(noticelist))
    update(db, chat_id, noticelist=str(noticelist))
    bot.send_message(chat_id, SUCCESS_ADDMEMBER % ' '.join(noticelist))


@bot.message_handler(commands=['setschedule'])
def setSchedule(message: Message):
    chat_id = message.chat.id
    if not room_in_database(db, chat_id):
        startMessage(message)
        return

    bot.send_message(message.chat.id, CALENDAR_SEND, reply_markup=create_calendar())
    update(db, chat_id, state='2')


@bot.callback_query_handler(func=lambda call: call.data.startswith("IGNORE") or
                                              call.data.startswith("DAY"))
def callback_query(call):
    chat_id = call.message.chat.id
    if not room_in_database(db, chat_id):
        startMessage(call.message)
        return

    chat = get_chat(db, chat_id)
    if chat['state'] == '2':
        result = process_calendar_selection(bot, call)
        update(db, chat_id, chosenday=result.__repr__(), state='1')

    else:
        bot.answer_callback_query(call.id)


@bot.message_handler(content_types=['text'])
def inPrivateMessage(message: Message):
    if message.from_user.id == message.chat.id:
        bot.send_message(message.chat.id, GO_TO_CHAT)
        return True
    return False


client = MongoClient(MONGO_URI)
db = client.heroku_2n5xgpck.roomBotBase

timeChecking = CheckTime()
timeChecking.start()
print(dir(calendar))
bot.infinity_polling()
import pymongo
import telebot
from telebot.types import Message
import os
from pymongo import MongoClient
import src
from pythoncalendar import create_calendar, process_calendar_selection, checkTime
from MESSAGES import *
from mongotools import *
from threading import Thread
import time


class CheckTime(Thread):
    def run(self):
        while 1:
            print("check time start!")
            checkTime(db, bot)
            time.sleep(60)

if "HEROKU" in list(os.environ.keys()):
    """
    If bot is started by heroku
    """

    TOKEN = os.getenv('BOT_TOKEN')
    MONGO_URI = os.getenv('MONGODB_URI')
else:
    """
    If bot started by my computer
    """

    from TOKENS import TOKEN, MONGO_URI

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['schedule'])
def sendSchedule(message: Message):
    chat_id = message.chat.id
    if not room_in_database(db, chat_id):
        startMessage(message)
        return

    url = "https://hotel.university.innopolis.ru/assets/images/schedule.png"
    name = src.saveScheduleImage(url)
    bot.send_photo(chat_id, src.getScheduleImage(name))


@bot.message_handler(commands=['start'])
def startMessage(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, START_MESSAGE)

    if not room_in_database(db, chat_id):
        createNew(db, chat_id)

@bot.message_handler(commands=['addmember'])
def addmembers(message: Message):
    chat_id = message.chat.id
    if not room_in_database(db, chat_id):
        startMessage(message)
        return

    aliases = message.text.split()
    if len(aliases) < 2:
        bot.send_message(chat_id, ADDMEMBER_ERORR)
        return

    chat = get_chat(db, chat_id)
    noticelist = eval(chat['noticelist'])
    noticelist.extend(aliases[1:])
    noticelist = list(set(noticelist))
    update(db, chat_id, noticelist=str(noticelist))
    bot.send_message(chat_id, SUCCESS_ADDMEMBER % ' '.join(noticelist))


@bot.message_handler(commands=['setschedule'])
def setSchedule(message: Message):
    chat_id = message.chat.id
    if not room_in_database(db, chat_id):
        startMessage(message)
        return

    bot.send_message(message.chat.id, CALENDAR_SEND, reply_markup=create_calendar())
    update(db, chat_id, state='2')


@bot.callback_query_handler(func=lambda call: call.data.startswith("IGNORE") or
                                              call.data.startswith("DAY"))
def callback_query(call):
    chat_id = call.message.chat.id
    if not room_in_database(db, chat_id):
        startMessage(call.message)
        return

    chat = get_chat(db, chat_id)
    if chat['state'] == '2':
        result = process_calendar_selection(bot, call)
        update(db, chat_id, chosenday=result.__repr__(), state='1')

    else:
        bot.answer_callback_query(call.id)


@bot.message_handler(content_types=['text'])
def inPrivateMessage(message: Message):
    if message.from_user.id == message.chat.id:
        bot.send_message(message.chat.id, GO_TO_CHAT)
        return True
    return False


client = MongoClient(MONGO_URI)
db = client.heroku_2n5xgpck.roomBotBase
print(dir(calendar))
timeChecking = CheckTime()
timeChecking.start()

bot.infinity_polling()
