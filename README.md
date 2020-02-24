# Room innopolis bot for everyday use 
> @sevenzing

Structure of the bot
---
+ docker-compose
   + python3
        + pyTelegramBotAPI 
        + flask  
        + mongotools
    + mongo

Logging
---
Bot logs in `/bot/roomBot.log`


Configuration
---
Replace field `bot_token` in `bot.config`. Configuration file is attached to bot via docker volumes.

Installation
---
1. Either using docker-compose
```bash
$ docker-compose up --build -d
```
2. or using python3
```bash
$ cd bot/
$ python3.6 -m pip install -r requirements.txt
$ python3.6 run.py
```

