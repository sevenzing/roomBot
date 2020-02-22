import sys

from roomBot import app
from roomBot.config import BOT_PORT


if __name__ == '__main__' and "--webhook" in sys.argv:
    app.run(host="0.0.0.0", port=int(BOT_PORT))