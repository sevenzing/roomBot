FROM python:latest

COPY notification/ notification/

COPY bot/requirements.txt notification/

COPY bot/roomBot/ notification/roomBot/

COPY bot/roomBot.log notification/

COPY bot.config ./


RUN pip3 install -r /notification/requirements.txt

RUN rm /notification/requirements.txt


WORKDIR ./notification

CMD touch notification.log

ENTRYPOINT ["python"]

CMD ["-u", "run.py"]
