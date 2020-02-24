import datetime
import pytz

from . import telegramtools
from . import mongotools
from . import tools
from .config import TIME_ZONE, NOTICE_MESSAGE_START, NOTICE_HOUR


def check_time(bot, db):
    now = datetime.datetime.now(pytz.timezone(TIME_ZONE))
    #now = datetime.datetime(2020, 2, 24, 7, 55, tzinfo=pytz.timezone(TIME_ZONE)) + datetime.timedelta(minutes=datetime.datetime.now(pytz.timezone(TIME_ZONE)).minute)
    
    _, week_number, day_number = now.isocalendar()
    if day_number not in [1, 3, 5] or now.hour < NOTICE_HOUR:
        return

    current_building = get_current_building(now)
    for chat in db.find({"checknotice": True}):
        print(chat)
        lastnotice = get_date_from_string(chat['lastnotice'])
        if now <= lastnotice:
            continue
        
        chat_id = chat['chat_id']
        if current_building == chat['chosenbuilding']:
            noticeMessage = NOTICE_MESSAGE_START

            telegramtools.send_message(bot, chat_id, noticeMessage)
            lastnotice = get_next_day(now)
            mongotools.update(db, chat_id, lastnotice=lastnotice.__repr__())
            tools.log(f"Sended notice message to {chat_id}. Updated lastnotice to {lastnotice}")
            

def get_date_from_string(string):
    return eval(string.replace(f"<StaticTzInfo '{TIME_ZONE}'>", f"pytz.timezone('{TIME_ZONE}')"))


def get_current_building(date: datetime.datetime):
    _, week_number, day_number = date.isocalendar()
    if day_number not in [1, 3, 5]:
        return 0
    
    order = [2, 3, 1, 4]
    return order[(order.index((order[2:4][::-1] + order[0:2][::-1])[(week_number - 1) % 4]) + (day_number - 1) // 2) % 4]


def get_next_cleaning_day(building):
    current_date = datetime.datetime.now(pytz.timezone(TIME_ZONE)) + datetime.timedelta(days=1) - datetime.timedelta(hours=NOTICE_HOUR)
    while get_current_building(current_date) != building:
        current_date += datetime.timedelta(days=1)
    return current_date


def daysLeft(date: datetime.datetime):
    return (date - datetime.datetime.now(pytz.timezone(TIME_ZONE))).days + 1

def getMonthName(date: datetime.datetime):
    return date.strftime("%B")

def get_next_day(date: datetime):
    n = date + datetime.timedelta(days=1)
    return datetime.datetime(n.year, n.month, n.day, tzinfo=pytz.timezone(TIME_ZONE))


if __name__ == "__main__":
    pass