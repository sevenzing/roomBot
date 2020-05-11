FROM python:latest

COPY bot/requirements.txt notification/

RUN pip3 install -r /notification/requirements.txt

RUN rm /notification/requirements.txt

COPY notification/ notification/

COPY bot/roomBot/ notification/roomBot/

COPY bot/roomBot.log notification/

WORKDIR ./notification

CMD touch notification.log

ENTRYPOINT ["sh"]

CMD ["run.sh"]
