from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from telebot import TeleBot
import telebot
import time
from roomBot import tools
from roomBot import config

def answer(bot: TeleBot, 
           message: Message, text: str, 
           parse_mode=None, reply_markup=None):

    time_start = time.time()
    sended_message = send_message(bot, message.chat.id, text, 
                                        parse_mode=parse_mode, 
                                        reply_markup=reply_markup)
    tools.log(f"BOT in {round(time.time() - time_start, 3)} -> {message.from_user.username}/{message.chat.id}: {text}")
    return sended_message


def send_message(bot: TeleBot, chat_id, text, parse_mode=None, reply_markup=None):
    try:
        time_start = time.time()
        tools.log(f"Trying to send message to {chat_id}")
        sended_message = bot.send_message(chat_id, text, parse_mode=parse_mode, reply_markup=reply_markup)
        tools.log(f"BOT in {round(time.time() - time_start, 3)} -> {chat_id}: {text}")
        return sended_message

    except telebot.apihelper.ApiException as e:
        error = e.args[0]
        print(error)
        if 'bot was kicked' in e.args[0]:
            tools.log(f"Bot has kicked from group {chat_id}.", error=True)
        else:
            raise(e)


def change_message(bot: TeleBot, message: Message, 
                   text=None, parse_mode=None, reply_markup=None):
    try:
        time_start = time.time()
        if not text is None:
            changed_message = bot.edit_message_text(text, message.chat.id, message.message_id, 
                                                    parse_mode=parse_mode, reply_markup=reply_markup)    
        elif not reply_markup is None:
            bot.edit_message_reply_markup(message.chat.id, message.message_id, reply_markup=reply_markup)
        
        tools.log(f"BOT [EDIT MESSAGE] in {round(time.time() - time_start, 3)} -> {message.chat.username}/{message.chat.id}: {text}")    
        return change_message
    except telebot.apihelper.ApiException as e:
        if 'bot was kicked' in e.args[0]:
            tools.log(f"Bot has kicked from group {message.chat.id}.", error=True)
        elif 'message is not modified' in e.args[0]:
            tools.log(f"Message not modified: {message}")
        else:
            raise(e)
        

def delete_message(bot: TeleBot, message: Message):
    bot.delete_message(message.chat.id, message.message_id)


def generate_choose_day_button() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    for number in range(1, 4, 2):
        keyboard.add(InlineKeyboardButton(f"{tools.ordinal(number)}", callback_data=f"__cb{number}"),
                     InlineKeyboardButton(f"{tools.ordinal(number + 1)}", callback_data=f"__cb{number + 1}"),)
    return keyboard


def generate_buy_list(buylist) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=2)
    
    for name in buylist:
        amount = buylist[name]
        
        name_button = telebot.types.InlineKeyboardButton(
            text = f"{tools.cut_text(name)}: [{amount}]",
            callback_data=f"change_menu|{config.INCREASE}|{name}")

        decr_button = telebot.types.InlineKeyboardButton(
            text = config.CHANGE_KEYBOARD_DECREASE_TEXT,
            callback_data=f"change_menu|{config.DECREASE}|{name}")
        
        keyboard.add(name_button, decr_button)

    close_button = telebot.types.InlineKeyboardButton(
            text = config.CHANGE_KEYBOARD_CLOSE_TEXT,
            callback_data=f"change_menu|{config.EXIT}|")

    clearlist_button = telebot.types.InlineKeyboardButton(
            text = config.CHANGE_KEYBOARD_CLEAR_TEXT,
            callback_data=f"change_menu|{config.CLEAR}|")
    
    keyboard.add(close_button, clearlist_button)

    return keyboard

def generate_empty_buttons():
    return InlineKeyboardMarkup()