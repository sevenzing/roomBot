from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from telebot import TeleBot
import telebot

from . import tools


def answer(bot: TeleBot, 
           message: Message, text: str, 
           parse_mode=None, reply_markup=None):
    try:
        sended_message = bot.send_message(message.chat.id, text, 
                                          parse_mode=parse_mode, 
                                          reply_markup=reply_markup)
        tools.log(f"BOT -> {message.from_user.username}/{message.chat.id}: {text}")

        return sended_message
    except telebot.apihelper.ApiException as e:
        if 'bot was kicked' in e.args[0]:
            raise Exception(f"Bot has kicked from group {message.chat.id}.")
        else:
            raise e


def send_message(bot: TeleBot, chat_id, text):
    try:
        sended_message = bot.send_message(chat_id, text, parse_mode="Markdown")
        tools.log(f"BOT -> {chat_id}: {text}")
        return sended_message

    except telebot.apihelper.ApiException as e:
        if 'bot was kicked' in e.args[0]:
            tools.log(f"Bot has kicked from group {chat_id}.", error=True)
        else:
            raise(e)


def change_message(bot: TeleBot, message: Message, 
                   text=None, parse_mode=None, reply_markup=None):
    try:
        if not text is None:
            changed_message = bot.edit_message_text(text, message.chat.id, message.message_id, parse_mode=parse_mode)
            tools.log(f"BOT [EDIT MESSAGE] -> {message.chat.username}/{message.chat.id}: {text}")
        if not reply_markup is None:
            bot.edit_message_reply_markup(message.chat.id, message.message_id, reply_markup=reply_markup)
            
        return change_message
    except telebot.apihelper.ApiException as e:
        if 'bot was kicked' is e.args[0]:
            tools.log(f"Bot has kicked from group {message.chat.id}.", error=True)
        else:
            raise(e)
        

def generate_choose_day_button():
    keyboard = InlineKeyboardMarkup(row_width=2)
    for number in range(1, 4, 2):
        keyboard.add(InlineKeyboardButton(f"{tools.ordinal(number)}", callback_data=f"__cb{number}"),
                     InlineKeyboardButton(f"{tools.ordinal(number + 1)}", callback_data=f"__cb{number + 1}"),)
    return keyboard