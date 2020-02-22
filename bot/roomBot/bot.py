import os
import telebot
from telebot.types import Message

from . import telegramtools
from . import config
from . import tools
from . import mongotools
from .mongotools import db


bot = telebot.TeleBot(config.BOT_TOKEN)


@bot.message_handler(func=lambda message: not message.new_chat_member is None,
                     content_types = ['new_chat_members'])    
def check_for_adding(message: telebot.types.Message):
    """
    Someone was added to a group
    """
    mongotools.createNew(db, message.chat.id, message.from_user.username)   


@bot.message_handler(commands=['start', 'help', 'schedule'])
def process_commands(message):
    """
    User sent a command to get information
    """

    mongotools.createNew(db, message.chat.id, message.from_user.username)

    if message.text in ['/start', '/help']: 
        telegramtools.answer(bot, message, config.START_MESSAGE)
    
    if message.text in ['/start']:
        change_building(message)

    if message.text in ['/schedule']:
        telegramtools.answer(bot, message, config.URL_TO_SCHEDULE)


@bot.message_handler(commands=['changebuilding'])
def change_building(message: Message):
    telegramtools.answer(bot, message, config.CHANGE_BUILDING_MESSAGE, reply_markup=telegramtools.generate_choose_day_button())


@bot.message_handler(commands=["nextcleaning"])
def sendNextCleaningDay(message: Message):
    message_to_send = tools.next_cleaning_day(db, message.chat.id)
    telegramtools.answer(bot, message, message_to_send, parse_mode='Markdown')



@bot.callback_query_handler(func=lambda call: call.data.startswith("__cb"))
def callback_query(call):
    """
    User has choosen building. call.data is "__cb{building number}"
    """

    # Remove __cb from message
    building = int(call.data[4:])

    mongotools.update(db, call.message.chat.id, chosenbuilding=building, checknotice=True)
    telegramtools.change_message(bot, call.message, 
                                 text=config.SUCCESS_BUILDING % tools.ordinal(building))







