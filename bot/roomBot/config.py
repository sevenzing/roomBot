import configparser

# --------
# Messages
# --------

START_MESSAGE = "Hi! I'm a room bot. I can do some useful things. \n\n"\
                "📅 First, select your building to understand the cleaning schedule\n"\
                "😎 If we are in a chat add all your roommates /addmembers\n"\
                "❓ When the next cleaning day? /nextcleaning\n"\
                "⏰ The bot sends a notification on every cleaning day at 8am \n"\
                "⏩ Did you make a mistake? Change your building /changebuilding \n"

HELP_MESSAGE = """help message"""

CHANGE_BUILDING_MESSAGE = "🏣 Please, select your building\n"

NOTICE_MESSAGE_START = "Hello! Don't forget about cleaning today!"

ADDMEMBER_ERORR = "Specify aliases after the command. \nFor example: /addmember @me @myfriend @myfriend2"

SUCCESS_ADDMEMBER = "Great! Now you have \n%s \nin your notice list"

NEXT_DAY = "Your building is %s, so the next cleaning day will be in *%d days*, on the *%s of %s*.\n"

SUCCESS_BUILDING = "Great! You have chosen %s building"

HAVE_NOT_BUILDING = "You haven't chosen a building yet. \n/changebuilding"


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