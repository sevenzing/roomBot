
#!/usr/bin/env python3
#
# A library that allows to create an inline calendar keyboard.
# grcanosa https://github.com/grcanosa
#
"""
Base methods for calendar keyboard creation and processing.
"""
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup
import datetime
import calendar
from MESSAGES import *
from mongotools import update

def create_callback_data(action, year, month, day):
    """ Create the callback data associated to each button"""
    return ";".join([action, str(year), str(month), str(day)])


def separate_callback_data(data):
    """ Separate the callback data"""
    return data.split(";")


def create_calendar(currentYear=None, currentMonth=None, currentDay=None):
    """
    Большой и огромный костыль.
    """

    now = datetime.datetime.now()
    if currentYear is None:
        currentYear = now.year
    if currentMonth is None:
        currentMonth = now.month
    if currentDay is None:
        currentDay = now.day

    data_ignore = create_callback_data("IGNORE", currentYear, currentMonth, 0)
    keyboard = InlineKeyboardMarkup()
    keyboard.row_width = 7

    # First row - Month and Year
    row = []
    row.append(
        InlineKeyboardButton(calendar.month_name[currentMonth] + " " + str(currentYear), callback_data=data_ignore))
    keyboard.add(*row)
    # Second row - Week Days
    row = []
    for day in ["Mo", "Tu", "We", "Th", "Fr", "Sa", "Su"]:
        row.append(InlineKeyboardButton(day, callback_data=data_ignore))
    keyboard.add(*row)

    thisMonth = calendar.monthcalendar(currentYear, currentMonth)
    nextMonth = calendar.monthcalendar(currentYear + currentMonth//12, currentMonth%12 + 1)

    if thisMonth[-1][-1] == 0:
        a = thisMonth[-1]
        b = nextMonth[0]
        c = [i for i in (a + b) if i != 0]
        thisMonth[-1] = c
        nextMonth.pop(0)

    my_calendar = thisMonth + nextMonth
    #print(my_calendar)
    for i in range(len(my_calendar)):
        if currentDay in my_calendar[i]:
            for _ in range(2):
                row = []
                for day in my_calendar[i]:
                    if (day == 0):
                        row.append(InlineKeyboardButton(" ", callback_data=data_ignore))
                    else:
                        row.append(InlineKeyboardButton(str(day), callback_data=create_callback_data("DAY", currentYear,
                                                                                                     currentMonth,
                                                                                                     day)))
                keyboard.add(*row)

                i += 1
            break

    return keyboard


def process_calendar_selection(bot, call):
    """
    Process the callback_query. This method generates a new calendar if forward or
    backward is pressed. This method should be called inside a CallbackQueryHandler.
    :param telegram.Bot bot: The bot, as provided by the CallbackQueryHandler
    :param telegram.Update update: The update, as provided by the CallbackQueryHandler
    :return: Returns a tuple (Boolean,datetime.datetime), indicating if a date is selected
                and returning the date if so.
    """

    action, year, month, day = separate_callback_data(call.data)

    if action == "IGNORE":
        bot.answer_callback_query(call.id)
        return None

    elif action == "DAY":
        result = datetime.datetime(int(year), int(month), int(day))
        nextCleaningDay = getNextCleaningDay(result)
        bot.send_message(call.message.chat.id, DAY_CHOOSE % f"{nextCleaningDay.day}/{nextCleaningDay.month}")
        bot.answer_callback_query(call.id, DAY_CHOOSE % f"{nextCleaningDay.day}/{nextCleaningDay.month}")
        bot.edit_message_text(text=TEXT_AFTER_SELECTION,
                              chat_id=call.message.chat.id,
                              message_id=call.message.message_id,
                              reply_markup=None)

        return result


def getNextCleaningDay(prev_date):
    prev_year = prev_date.year
    prev_month = prev_date.month
    prev_day = prev_date.day

    thisMonth = calendar.monthcalendar(prev_year, prev_month)
    nextMonth = calendar.monthcalendar(prev_year + prev_month//12, prev_month%12 + 1)

    if thisMonth[-1][-1] == 0:
        a = thisMonth[-1]
        b = nextMonth[0]
        c = [i for i in (a + b) if i != 0]
        thisMonth[-1] = c
        nextMonth.pop(0)

    my_calendar = thisMonth + nextMonth
    for i in range(len(my_calendar)):
        if prev_day in my_calendar[i]:
            targetDay = my_calendar[i + 1][(datetime.datetime.weekday(prev_date) + 2) % 6]
            targetYear = prev_year
            targetMonth = prev_month
            if targetDay < my_calendar[i][0]:
                targetMonth += 1
                if targetMonth > 12:
                    targetMonth = 1
                    targetYear += 1

            break

    return datetime.datetime(targetYear, targetMonth, targetDay)

def checkTime(db, bot):
    now = datetime.datetime.now()
    #now = datetime.datetime(2019, 12, 4, 8)
    currentYear = now.year
    currentMonth = now.month
    currentDay = now.day


    for chat in db.find({"checknotice": True}):
        prev_date = eval(chat['chosenday'])
        if prev_date is None:
            return



        nextCleaningDay = getNextCleaningDay(prev_date)
        if currentYear >= nextCleaningDay.year and \
                currentMonth >= nextCleaningDay.month and \
                currentDay >= nextCleaningDay.day and now.hour >= 8:

            print('asd')

            noticelist = eval(chat['noticelist'])
            noticeMessage = NOTICE_MESSAGE_START
            print(noticelist)
            for alias in noticelist:
                noticeMessage += f'\n{alias}'

            bot.send_message(chat['chat_id'], noticeMessage)

            update(db, chat['chat_id'], chosenday=nextCleaningDay.__repr__())
    print(f"Time has been checked. Current time is {now}")

def getMonthName(date: datetime.datetime):
    return date.strftime("%B")

if __name__ == "__main__":
    date = datetime.datetime(2019, 12, 2)
    print(getNextCleaningDay(date))