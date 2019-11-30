import pymongo

default_user = {'chat_id': None,
                'state': '0',
                'chosenday': 'None',
                'noticelist': '[]',
                'checknotice': True}

def createNew(db, id):
    user = default_user.copy()

    user['chat_id'] = id
    db.insert_one(user)


def get_chat(db, chat_id):
    user = None
    for i in db.find({'chat_id': chat_id}):
        user = i
        break

    return user


def update(db, chat_id, state=None, chosenday=None, noticelist=None):
    new_user_options = {}
    for i, option in enumerate([chat_id, state, chosenday, noticelist]):
        if option is not None:
            new_user_options[list(default_user.keys())[i]] = option

    db.update_one({'chat_id': chat_id}, {'$set': new_user_options})


def room_in_database(db, chat_id):
    if get_chat(db, chat_id) is None:
        return False
    return True


if __name__ == '__main__':
    from TOKENS import MONGO_URI

    client = pymongo.MongoClient(MONGO_URI)


    db = client.heroku_2n5xgpck.roomBotBase

    print(dir(db))
    for i in db.find({"checknotice": True}):
        pass