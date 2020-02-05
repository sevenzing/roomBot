# --------
# Messages
# --------

START_MESSAGE = """Hi! I'm a room bot. I can do some useful things. \n\n📅 First, select your building to understand the cleaning schedule\n😎 If we are in a chat add all your roommates /addmembers\n❓ When the next cleaning day? /nextcleaning\n⏰ The bot sends a notification on every cleaning day at 8am \n⏩ Did you make a mistake? Change your building /changebuilding \n"""

CHANGE_BUILDING_MESSAGE = """🏣 Please, select your building\n"""

NOTICE_MESSAGE_START = """Hello! Don't forget about cleaning today!"""

ADDMEMBER_ERORR = """Specify aliases after the command. \nFor example: /addmember @me @myfriend @myfriend2"""

SUCCESS_ADDMEMBER = """Great! Now you have \n%s \nin your notice list"""

NEXT_DAY = """Your building is %s, so the next cleaning day will be the *%s of %s*"""

SUCCESS_BUILDING = """Great! You have chosen %s building"""

HAVE_NOT_BUILDING = "You haven't chosen a building yet. \n/changebuilding"

# ---------
# Variables
# ---------

NOTICE_HOUR = 8

TIME_ZONE = 'Etc/GMT-3'
