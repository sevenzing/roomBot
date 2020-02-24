from datetime import datetime, timedelta
import pymongo
import pytz

from .config import TIME_ZONE, NOTICE_HOUR


def get_db():
    client = pymongo.MongoClient('mongodb://root:password@mongo:27017/')
    db = client.user1448

    #client = pymongo.MongoClient('mongodb://heroku_2n5xgpck:hfoqb10p4b1968cv42nbrsrlef@ds031359.mlab.com:31359/heroku_2n5xgpck?retryWrites=false')

    #return client.heroku_2n5xgpck.roomBotTest3
    return db.roomBot


default_chat = {'chat_id': None,
                'username': None,
                'chosenbuilding': 0,
                'checknotice': True,
                'lastnotice': None}

db = get_db()


def createNew(db, chat_id, username=None, chosenbuilding=0):

    if chat_in_database(db, chat_id):
        return 

    chat = default_chat.copy()

    chat['chat_id'] = chat_id
    chat['chosenbuilding'] = chosenbuilding
    chat['username'] = username
    chat['lastnotice'] = get_next_day(datetime.now(pytz.timezone(TIME_ZONE)) - timedelta(hours=NOTICE_HOUR)).__repr__()
    db.insert_one(chat)


def get_chat(db, chat_id):
    chat = None
    for chat_iter in db.find({'chat_id': chat_id}):
        chat = chat_iter
        break

    return chat


def update(db, chat_id, username=None, chosenbuilding=None, checknotice=None, lastnotice=None):
    if not chat_in_database(db, chat_id):
        createNew(db, chat_id, chosenbuilding=chosenbuilding)
    
    new_user_options = {}
    for option_name, option in zip(['username', 'chosenbuilding', 'checknotice', 'lastnotice'],
                                   [username, chosenbuilding, checknotice, lastnotice]):
        if not option is None:
            new_user_options[option_name] = option

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