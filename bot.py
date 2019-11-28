import telebot
from telebot.types import Message
import os
from flask import Flask, request
import logging

token = '982620066:AAESmASPIDYIM7bGOyCCl6r8cmO7r5qTuSo'
bot = telebot.TeleBot(token)

# Здесь пишем наши хэндлеры

# Проверим, есть ли переменная окружения Хероку (как ее добавить смотрите ниже)

@bot.message_handler(content_types=['text'])
def jopa(message: Message):
	bot.send_message(message.chat.id, message.text)

if "HEROKU" in list(os.environ.keys()):
    logger = telebot.logger
    telebot.logger.setLevel(logging.INFO)

    server = Flask(__name__)
    @server.route("/bot", methods=['POST'])
    def getMessage():
        bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
        return "!", 200

    @server.route("/")
    def webhook():
        bot.remove_webhook()
        bot.set_webhook(url="https://tgbot1234.herokuapp.com/") # этот url нужно заменить на url вашего Хероку приложения
        return "?", 200
    print(f"Bot has started by webhook.")
    server.run(host="0.0.0.0", port=os.environ.get('PORT', 80))
else:
    # если переменной окружения HEROKU нету, значит это запуск с машины разработчика.
    # Удаляем вебхук на всякий случай, и запускаем с обычным поллингом.
    bot.remove_webhook()
    print(f"Bot has started by polling.")
    bot.polling(none_stop=True)