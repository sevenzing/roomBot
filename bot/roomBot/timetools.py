import datetime
import pytz
import time
from threading import Thread

from roomBot import telegramtools
from roomBot import database
from roomBot import tools
from .config import TIME_ZONE, NOTICE_MESSAGE_START, NOTICE_HOUR


def get_next_day(date: datetime):
    n = date + datetime.timedelta(days=1)
    return datetime.datetime(n.year, n.month, n.day, tzinfo=pytz.timezone(TIME_ZONE))


def get_date_from_string(string):
    return eval(string.replace(f"<StaticTzInfo '{TIME_ZONE}'>", f"pytz.timezone('{TIME_ZONE}')"))


def get_current_building(date: datetime.datetime):
    _, week_number, day_number = date.isocalendar()
    if day_number not in [1, 3, 5]:
        return 0
    order = [1, 4, 2, 3]
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



if __name__ == "__main__":
    pass