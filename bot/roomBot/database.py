from datetime import datetime, timedelta
import redis
import pytz
from typing import List, Dict, Union
import json

from .config import TIME_ZONE, NOTICE_HOUR
from . import tools

def get_db():
    db = redis.Redis(host='redis', port=5432)
    return db


default_chat = {'chat_id': None,
                'username': None,
                'state': 0,
                'chosenbuilding': 0,
                'checknotice': True,
                'lastnotice': None,
                'buylist':{"Sample": 1}}

db = get_db()


def createNew(chat_id, username=None, chosenbuilding=0):

    if chat_in_database(chat_id):
        return 

    chat = default_chat.copy()

    chat['chat_id'] = chat_id
    chat['chosenbuilding'] = chosenbuilding
    chat['username'] = username
    chat['lastnotice'] = get_next_day(datetime.now(pytz.timezone(TIME_ZONE)) - timedelta(hours=NOTICE_HOUR)).__repr__()
    
    insert_chat(chat_id, chat)

def insert_chat(key: Union[str, int], value: dict):
    assert isinstance(value, dict)
    
    db.set(key, json.dumps(value))


def get_chat(chat_id) -> Dict:
    value = db.get(chat_id)

    if value:
        return json.loads(value.decode()) 
    else:
        return None

def find(dct):
    for chat_id in [c.decode() for c in db.keys()]:
        chat = get_chat(chat_id)
        suitable = True
        for attribute in dct:
            if attribute not in chat:
                suitable = False
                break
            if chat[attribute] != dct[attribute]:
                suitable = False
                break
        if suitable: 
            yield chat

def find_chats_with_notice() -> Dict:
    for chat in find({"checknotice": True}):
        yield chat


def update(chat_id, username=None, state=None, chosenbuilding=None, checknotice=None, lastnotice=None, buylist=None):
    if not chat_in_database(chat_id):
        createNew(chat_id, chosenbuilding=chosenbuilding)
    
    chat = get_chat(chat_id)
    for name, value in zip(['username', 'state', 'chosenbuilding', 'checknotice', 'lastnotice', 'buylist'],
                           [ username,   state,   chosenbuilding,   checknotice,   lastnotice,   buylist]):
        if value != None:
            chat[name] = value
    insert_chat(chat_id, chat)

    
def chat_in_database(chat_id):
    return db.exists(chat_id)


def get_next_day(date: datetime):
    n = date + timedelta(days=1)
    return datetime(n.year, n.month, n.day, tzinfo=pytz.timezone(TIME_ZONE))


def extend_buy_list(chat_id, message):
    buylist = get_safe(chat_id, 'buylist')
    all_names = {item[0] for item in buylist}

    for item_name in message.split('\n'):
        item_name = tools.cut_text(item_name)
        if item_name not in all_names:
            buylist[item_name] = 1
            all_names.add(item_name)
        else:
            buylist[item_name] += 1
    update(chat_id, buylist=buylist)


def get_safe(chat_id, key):
    chat = get_chat(chat_id)
    if chat is None:
        return default_chat[key]
    return chat[key]


def change_amount_of_items(chat_id, item_name, number) -> bool:
    # search for item
    buylist = get_safe(chat_id, 'buylist')
    
    if item_name in buylist:
        amount = buylist[item_name]
        # update amount
        if amount + number <= 0:
            buylist.pop(item_name)
        else:
            buylist[item_name] += amount 

        update(chat_id, buylist=buylist)
        return True

    return False
