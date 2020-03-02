import sys
import telebot
from telebot.types import Message

from . import telegramtools
from . import config
from . import tools
from . import mongotools
from . import timetools

bot = telebot.TeleBot(config.BOT_TOKEN)

def start():
    tools.log(f'Hello from @{bot.get_me().username}!')

    bot.delete_webhook()
    tools.log('[INFO] >> Removed webhook')

    from .mongotools import db
    tools.log('[INFO] >> Database has been attached')

    if "--webhook" in sys.argv:
        tools.log("[INFO] >> Setting webhook")
        tools.log("webhook not implemented yet. Exit...")
        exit(1)
    else:
        tools.log('[INFO] >> Starting polling ...')
        bot.polling()


@bot.message_handler(func=lambda message: not message.new_chat_member is None,
                     content_types = ['new_chat_members'])    
def check_for_adding(message: telebot.types.Message):
    """
    Someone was added to a group
    """
    mongotools.createNew(message.chat.id, message.from_user.username)   


@bot.message_handler(commands=['start', 'help', 'schedule'])
def process_commands(message):
    """
    User sent a command to get information
    """

    mongotools.createNew(message.chat.id, message.from_user.username)

    if message.text in ['/start', '/help']: 
        telegramtools.answer(bot, message, config.START_MESSAGE)
    
    if message.text in ['/start']:
        change_building(message)

    if message.text in ['/schedule']:
        telegramtools.answer(bot, message, config.URL_TO_SCHEDULE)


@bot.message_handler(commands=['changebuilding'])
def change_building(message: Message):
    telegramtools.answer(bot, message, config.CHANGE_BUILDING_MESSAGE, 
                         reply_markup=telegramtools.generate_choose_day_button())


@bot.message_handler(commands=['nextcleaning'])
def sendNextCleaningDay(message: Message):
    message_to_send = tools.next_cleaning_day(message.chat.id)
    telegramtools.answer(bot, message, message_to_send, parse_mode='Markdown')


@bot.message_handler(commands=['list'])
def sendBuyList(message: Message):
    buylist = mongotools.get_safe(message.chat.id, 'buylist')
    telegramtools.answer(bot, message, config.SEND_BUY_LIST, 
                         reply_markup=telegramtools.generate_buy_list(buylist))


@bot.message_handler(commands=['add'])
def setStateToAdd(message: Message):
    mongotools.update(message.chat.id, state=tools.States.STATE_WAIT_FOR_ADD)
    telegramtools.answer(bot, message, config.ADD_ITEM_TO_LIST, parse_mode='Markdown')


@bot.message_handler(func=lambda m: mongotools.get_safe(m.chat.id, 'state') == tools.States.STATE_WAIT_FOR_ADD)
def addMessageToList(message: Message):
    mongotools.extend_buy_list(message.chat.id, message.text)
    mongotools.update(message.chat.id, state=tools.States.STATE_DEFAULT)
    telegramtools.send_message(bot, message.chat.id, config.ITEMS_ADDED)


@bot.callback_query_handler(func=lambda call: call.data.startswith('__cb'))
def callback_query(call):
    """
    User has choosen building. call.data is "__cb{building number}"
    """

    # Remove __cb from message
    building = int(call.data[4:])

    mongotools.update(call.message.chat.id, chosenbuilding=building, checknotice=True)
    telegramtools.change_message(bot, call.message, 
                                 text=config.SUCCESS_BUILDING % tools.ordinal(building))


@bot.callback_query_handler(func=lambda call: 'change_menu' in call.data)
def change_query_handler(call):
    tools.proccess_change_menu(bot, call)
    


