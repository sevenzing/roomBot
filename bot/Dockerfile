FROM python:latest

COPY bot/ bot/

COPY bot.config ./

RUN pip3 install -r /bot/requirements.txt


RUN rm /bot/requirements.txt

WORKDIR ./bot

CMD touch notification.log

ENTRYPOINT ["python"]

CMD ["-u", "run.py"]
