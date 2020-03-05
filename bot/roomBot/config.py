import configparser

PATH_TO_BOT_LOG_FILE = 'roomBot.log'
PATH_TO_NOTIFICATION_LOG_FILE = 'notification.log'

# ========
# Messages
# ========

START_MESSAGE = "Hi! I'm room bot. \n\n"\
                "📅 First, select your building to understand the cleaning schedule\n"\
                "😎 You can /add item to your buylist and manage it using /list\n"\
                "❓ When the next cleaning day? /nextcleaning\n"\
                "⏩ Did you make a mistake? Change your building /changebuilding \n"\
                "⏰ The bot sends a notification on every cleaning day at 8am \n"\

HELP_MESSAGE = """help message"""

CHANGE_BUILDING_MESSAGE = "🏣 Please, select your building\n"

NOTICE_MESSAGE_START = "Hello! Don't forget about cleaning today!"

NEXT_DAY = "Your building is %s, so the next cleaning day will be in *%d days*, on the *%s of %s*.\n"

SUCCESS_BUILDING = "Great! You have chosen %s building"

HAVE_NOT_BUILDING = "You haven't chosen a building yet. \n/changebuilding"

# ==========
#  Buy list 
# ==========

SEND_BUY_LIST = "Your list:"

CHANGE_KEYBOARD_DECREASE_TEXT = "/Decrease/"

CHANGE_KEYBOARD_CLOSE_TEXT = "/Close/"

CHANGE_KEYBOARD_CLEAR_TEXT = "/Clear/"

ADD_ITEM_TO_LIST = "Specify the items you want to buy like this:*\nitem1\nitem number 2\nitem #3*"

LIST_WAS_DELETED = "The list was cleared"

ITEMS_ADDED = "Acknowledged, %s"

# -- | Callback data

INCREASE = 'increase'

DECREASE = 'decrease'

EXIT = 'exit'

CLEAR = 'clear'

# =================
#  FROM CONFIG FILE
# =================


CONFIG_NAME = "Bot settings" 
PATH = "../bot.config"


def readConfig(path, name):
    values = {"bot_token": None,
              "time_zone": None,
              "notice_hour": None,
              "url_to_schedule": None,
              "bot_port": None,
              "bot_url": None}
    
    config = configparser.ConfigParser()
    config.read(path)
    
    for key in values:
        values[key] = (config.get(name, key))
    
    return values
 
BOT_TOKEN, TIME_ZONE, NOTICE_HOUR, URL_TO_SCHEDULE, BOT_PORT, BOT_URL  = readConfig(PATH, CONFIG_NAME).values()

NOTICE_HOUR = int(NOTICE_HOUR)