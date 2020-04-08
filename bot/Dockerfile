FROM python:latest

COPY bot/requirements.txt bot/requirements.txt 

RUN pip3 install -r /bot/requirements.txt

RUN rm bot/requirements.txt

COPY bot/ bot/

WORKDIR bot

CMD touch notification.log

ENTRYPOINT ["sh"]

CMD ["run.sh"]
