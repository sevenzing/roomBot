import datetime
import pytz
from setup import logger 

# docker will copy this module  
from roomBot import mongotools, timetools, config, tools, telegramtools


def check_time(bot, db):

    now = datetime.datetime.now(pytz.timezone(config.TIME_ZONE))
    #now = datetime.datetime(2020, 3, 4, 7, 55, tzinfo=pytz.timezone(config.TIME_ZONE)) + datetime.timedelta(minutes=datetime.datetime.now(pytz.timezone(config.TIME_ZONE)).minute)
    
    _, week_number, day_number = now.isocalendar()
    if day_number not in [1, 3, 5] or now.hour < config.NOTICE_HOUR:
        return

    current_building = timetools.get_current_building(now)
    for chat in mongotools.find_chats_with_notice():
        lastnotice = timetools.get_date_from_string(chat['lastnotice'])
        if now <= lastnotice:
            continue
        
        chat_id = chat['chat_id']
        if current_building == chat['chosenbuilding']:
            noticeMessage = config.NOTICE_MESSAGE_START

            telegramtools.send_message(bot, chat_id, noticeMessage)
            lastnotice = timetools.get_next_day(now)
            mongotools.update(chat_id, lastnotice=lastnotice.__repr__())
            log(f"Sended notice message to {chat['username']}/{chat_id}. Updated lastnotice to {lastnotice}")

    

def log(message):
    logger.info(message)
    print(message)
