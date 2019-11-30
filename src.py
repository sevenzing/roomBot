import requests
import math

def saveScheduleImage(url, name='schedule.png') -> str:
    file = open(name, 'wb')
    p = requests.get(url)
    file.write(p.content)
    file.close()
    return name


def getScheduleImage(path):
    file = open(path, 'rb')
    return file


def ordinal(n):
    return "%d%s" % (n, "tsnrhtdd"[(math.floor(n / 10) % 10 != 1) * (n % 10 < 4) * n % 10::4])



if __name__ == "__main__":
    url = "https://hotel.university.innopolis.ru/assets/images/schedule.png"
    getScheduleImage(url)
