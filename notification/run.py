import time
from setup import bot, db
import timechecking


if __name__ == "__main__":
    counter = 0
    while 1:
        if counter == 0:
            timechecking.log("Time checking...")

        timechecking.check_time(bot, db)
        counter = (counter + 1) % 10
        
        time.sleep(60)
        
        