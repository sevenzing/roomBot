import requests

from roomBot.bot import start, bot
from roomBot import tools
from roomBot.telegramtools import send_message
from roomBot.config import BOT_ADMIN

import argparse

parser = argparse.ArgumentParser()
parser.add_argument ('--start', action='store_true')


parser.add_argument('--send-message', type=str, nargs=1,
                    help='message to send to bot admin')


args = parser.parse_args()

if __name__ == "__main__":

    if args.start:
        try:
            start()

        except (requests.exceptions.ReadTimeout, requests.exceptions.ConnectionError) as e:
            tools.log(e, error=True)
            exit(137)
            
        except Exception as e:
            tools.log(e, error=True)
            exit(1)
    
    elif args.send_message:
        send_message(bot, BOT_ADMIN, args.send_message[0])