import flask
import telebot
import sys
import time
from threading import Thread

from . import tools


class CheckTime(Thread):
    def run(self):
        count = 100
        while 1:
            
            count += 1
            if count > 100:
                count = 0
                
                timetools.check_time(bot, db)
                tools.log("Checked time")

            time.sleep(1)
                 
app = flask.Flask(__name__)


from .bot import bot
tools.log(f'Hello from @{bot.get_me().username}!')
bot.delete_webhook()
tools.log('[INFO] >> Removed webhook')
from .mongotools import db
tools.log('[INFO] >> Database has been attached')
timeChecking = CheckTime()
timeChecking.start()
tools.log("[INFO] >> Time checking started.")

if "--webhook" in sys.argv:
    tools.log("[INFO] >> Setting webhook")
    tools.log("webhook not implemented yet. Exit...")
    exit(1)
else:
    tools.log('[INFO] >> Starting polling ...')
    try:
        bot.polling()
    except Exception as e:
        tools.log(e, error=True)
        raise e


@app.route('/', methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)