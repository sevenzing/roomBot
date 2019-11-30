import requests




def saveScheduleImage(url, name='schedule.png') -> str:
    file = open(name, 'wb')
    p = requests.get(url)
    file.write(p.content)
    file.close()
    return name


def getScheduleImage(path):
    file = open(path, 'rb')
    return file


if __name__ == "__main__":
    url = "https://hotel.university.innopolis.ru/assets/images/schedule.png"
    getScheduleImage(url)
