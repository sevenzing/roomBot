from datetime import datetime, timedelta
import pymongo
import pytz
from typing import List, Dict

from .config import TIME_ZONE, NOTICE_HOUR


def get_db():
    client = pymongo.MongoClient('mongodb://root:password@mongo:27017/')
    db = client.user1448

    #client = pymongo.MongoClient('mongodb://heroku_2n5xgpck:hfoqb10p4b1968cv42nbrsrlef@ds031359.mlab.com:31359/heroku_2n5xgpck?retryWrites=false')

    #return client.heroku_2n5xgpck.roomBotTest3
    return db.roomBot


default_chat = {'chat_id': None,
                'username': None,
                'state': 0,
                'chosenbuilding': 0,
                'checknotice': True,
                'lastnotice': None,
                'buylist':[("example of your items", 1)]}

db = get_db()

def createNew(chat_id, username=None, chosenbuilding=0):

    if chat_in_database(chat_id):
        return 

    chat = default_chat.copy()

    chat['chat_id'] = chat_id
    chat['chosenbuilding'] = chosenbuilding
    chat['username'] = username
    chat['lastnotice'] = get_next_day(datetime.now(pytz.timezone(TIME_ZONE)) - timedelta(hours=NOTICE_HOUR)).__repr__()
    db.insert_one(chat)


def get_chat(chat_id) -> Dict:
    chat = None
    for chat_iter in db.find({'chat_id': chat_id}):
        chat = chat_iter
        break

    return chat


def find_chats_with_notice() -> Dict:
    for chat in db.find({"checknotice": True}):
        yield chat


def update(chat_id, username=None, state=None, chosenbuilding=None, checknotice=None, lastnotice=None, buylist=None):
    if not chat_in_database(chat_id):
        createNew(chat_id, chosenbuilding=chosenbuilding)
    
    new_user_options = {}
    for option_name, option in zip(['username', 'state', 'chosenbuilding', 'checknotice', 'lastnotice', 'buylist'],
                                   [ username,   state,   chosenbuilding,   checknotice,   lastnotice,   buylist]):
        if not option is None:
            new_user_options[option_name] = option

    db.update_one({'chat_id': chat_id}, {'$set': new_user_options})


def chat_in_database(chat_id):
    return not get_chat(chat_id) is None


def get_next_day(date: datetime):
    n = date + timedelta(days=1)
    return datetime(n.year, n.month, n.day, tzinfo=pytz.timezone(TIME_ZONE))


def extend_buy_list(chat_id, message):
    buylist = get_safe(chat_id, 'buylist')
    all_names = {item[0] for item in buylist}

    for item_name in message.split('\n'):
        if item_name not in all_names:
            buylist.append([item_name, 1])
            all_names.add(item_name)
            
    update(chat_id, buylist=buylist)


def get_safe(chat_id, key):
    chat = get_chat(chat_id)
    if chat is None:
        createNew(chat_id)
    return chat[key]


def change_amount_of_items(chat_id, item_name, number) -> bool:
    # search for item
    buylist = get_safe(chat_id, 'buylist')
    for index in range(len(buylist)):
        name, amount = buylist[index]
        if name == item_name:            
            # update amount
            if amount + number <= 0:
                buylist.remove([name, amount])
            else:
                buylist[index] = (name, amount + number)

            update(chat_id, buylist=buylist)
            return True

    return False

if __name__ == '__main__':
    from TOKENS import MONGO_URI

    client = pymongo.MongoClient(MONGO_URI)


    db = client.heroku_2n5xgpck.roomBotBase

    for i in db.find({"checknotice": True}):
        pass