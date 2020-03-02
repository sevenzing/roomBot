from roomBot.bot import start
from roomBot import tools

try:
    start()
except Exception as e:
    tools.log(e, error=True)
    raise e
