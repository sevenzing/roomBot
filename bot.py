import telebot
import src

TOKEN = '982620066:AAESmASPIDYIM7bGOyCCl6r8cmO7r5qTuSo'
bot = telebot.TeleBot(TOKEN)


@bot.message_handler(content_types=['text'])
lambda x: src.start(x, bot)


bot.polling()
