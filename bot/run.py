import requests

from roomBot.bot import start
from roomBot import tools

try:
    start()

except requests.exceptions.ReadTimeout as e:
    tools.log(e, error=True)
    exit(137)
    
except Exception as e:
    tools.log(e, error=True)
    exit(1)
