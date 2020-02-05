FROM python:buster

WORKDIR ./

ENV BOT_TOKEN 1234:1234
ENV MONGOBD_URI mongodb://puthereyourtoken


COPY bot.py config.py Dockerfile mongotools.py telegramtools.py timetools.py tools.py requirements.txt ./

RUN pip3 install -r requirements.txt

CMD ["python", "-u", "bot.py"]
