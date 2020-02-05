import pymongo
from datetime import datetime, timedelta
import pytz
from config import TIME_ZONE, NOTICE_HOUR


default_chat = {'chat_id': None,
                'state': '0',
                'chosenbuilding': 0,
                'noticelist': '[]',
                'checknotice': True,
                'lastnotice': None}


def createNew(db, chat_id, chosenbuilding=None):
    chat = default_chat.copy()

    chat['chat_id'] = chat_id
    chat['chosenbuilding'] = chosenbuilding
    chat['lastnotice'] = get_next_day(datetime.now(pytz.timezone(TIME_ZONE)) - timedelta(hours=NOTICE_HOUR)).__repr__()
    db.insert_one(chat)


def get_chat(db, chat_id):
    chat = None
    for chat_iter in db.find({'chat_id': chat_id}):
        chat = chat_iter
        break

    return chat


def update(db, chat_id, state=None, chosenbuilding=None, noticelist=None, checknotice=None, lastnotice=None):
    new_user_options = {}
    for i, option in enumerate([chat_id, state, chosenbuilding, noticelist, checknotice, lastnotice]):
        if option is not None:
            new_user_options[list(default_chat.keys())[i]] = option

    db.update_one({'chat_id': chat_id}, {'$set': new_user_options})


def chat_in_database(db, chat_id):
    return not get_chat(db, chat_id) is None


def get_next_day(date: datetime):
    n = date + timedelta(days=1)
    return datetime(n.year, n.month, n.day, tzinfo=pytz.timezone(TIME_ZONE))


def extend_notice_list(db, chat_id, aliases):
    chat = get_chat(db, chat_id)
    noticelist = eval(chat['noticelist'])
    noticelist.extend(aliases)
    noticelist = list(set(noticelist))
    update(db, chat_id, noticelist=str(noticelist))
    return noticelist

if __name__ == '__main__':
    from TOKENS import MONGO_URI

    client = pymongo.MongoClient(MONGO_URI)


    db = client.heroku_2n5xgpck.roomBotBase

    for i in db.find({"checknotice": True}):
        pass