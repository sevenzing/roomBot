import time
from setup import bot, db
import timechecking

if __name__ == "__main__":
    while 1:
        timechecking.check_time(bot, db)
        time.sleep(60)
