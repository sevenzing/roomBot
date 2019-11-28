from telebot.types import Message

def start(message: Message, bot):
    print(type(message))
    bot.send_message(message.chat.id, 'kek')
    pass