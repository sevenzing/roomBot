from telebot.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from telebot import TeleBot
from tools import ordinal
import telebot


def generate_choose_day_button():
    keyboard = InlineKeyboardMarkup(row_width=2)
    for number in range(1, 4, 2):
        keyboard.add(InlineKeyboardButton(f"{ordinal(number)}", callback_data=f"__cb{number}"),
                     InlineKeyboardButton(f"{ordinal(number + 1)}", callback_data=f"__cb{number + 1}"),)
    return keyboard


def answer(bot: TeleBot, logger, 
           message: Message, text: str, 
           parse_mode=None, reply_markup=None):
    try:
        sended_message = bot.send_message(message.chat.id, text, 
                                          parse_mode=parse_mode, 
                                          reply_markup=reply_markup)

        logger.info(f"BOT -> {message.from_user.username}: {text}")
        return sended_message
    except telebot.apihelper.ApiException as e:
        if 'bot was kicked' in e.args[0]:
            logger.error(f"Bot has kicked from group {message.chat.id}.")
        else:
            raise(e)


def change_message(bot: TeleBot, logger,
                   message: Message, text=None,
                   parse_mode=None,
                   reply_markup=None):
    try:
        if not text is None:
            changed_message = bot.edit_message_text(text, message.chat.id, message.message_id, parse_mode=parse_mode)
        if not reply_markup is None:
            bot.edit_message_reply_markup(message.chat.id, message.message_id, reply_markup=reply_markup)
            
        return change_message
    except telebot.apihelper.ApiException as e:
        if 'bot was kicked' is e.args[0]:
            logger.error(f"Bot has kicked from group {message.chat.id}.")
        else:
            raise(e)


def send_notice(bot: TeleBot, logger, chat_id, text):
    try:
        sended_message = bot.send_message(chat_id, text, parse_mode="Markdown")
        logger.info(f"BOT -> {chat_id}: {text}")
        return sended_message

    except telebot.apihelper.ApiException as e:
        if 'bot was kicked' in e.args[0]:
            logger.error(f"Bot has kicked from group {chat_id}.")
        else:
            raise(e)
