import requests
from bs4 import BeautifulSoup
from models import *
from urllib.parse import urljoin
import re
from parsers import *


def fill_stations():
    url = r'https://www.tutu.ru/msk/'
    dirs = DirectionsParser(url).parse()

    for dir in dirs:

        stations = set()
        for st in StationsParser(urljoin(url, dir.url)).parse():
            stations.add(st)

        from db import get_database
        mongo = get_database(r'mongodb://localhost:27017')
        collection = mongo['stations']
        for s in stations:
            doc = vars(s)
            collection.replace_one({'_id': doc['_id']}, doc, upsert=True)


def fill_train():
    url = r'https://www.tutu.ru/view.php?np=053d70f6e5'
    train = TrainParser(url).parse()

    from db import get_database
    mongo = get_database(r'mongodb://localhost:27017')
    collection = mongo['trains']
    train.stations = [vars(s) for s in train.stations]
    doc = vars(train)
    collection.replace_one({'_id': doc['_id']}, doc, upsert=True)


def get_schedule():
    url = r'https://www.tutu.ru/station.php?nnst=83511'
    links = ScheduleParser(url).parse()

    print(links)


if __name__ == '__main__':
    get_schedule()
