import db
import conf
from parsers import *
from urllib.parse import urljoin
from types import SimpleNamespace

import logging
_module_name = 'scrape'
_log = getLogger(_module_name)
_log.setLevel(logging.INFO)

def update_stations():
    url = urljoin(conf.URL, 'msk')
    directions = DirectionsParser(url).parse()

    for d in directions:
        stations = set()
        direction_url = urljoin(url, d.url)
        for station in StationsParser(direction_url).parse():
            stations.add(station)

        subway_station = list(filter(lambda x: x.subway, stations))[:1]
        if subway_station:
            d.subway = subway_station[0]

        _log.info(f'found {len(stations)} at direction {d.name}')
        collection = db.get_collection('stations')

        db.replace_many(collection, [vars(s) for s in stations])


def update_trains_old():
    stations = db.get_collection('stations')
    scrape_queue = set()
    for station_dict in stations.find():
        station = Station(**station_dict)
        scrape_queue.add(station._id)

    _log.info(f'stations in queue: {len(scrape_queue)}')

    size_before_scrape = -1
    while scrape_queue and size_before_scrape != len(scrape_queue):
        station = scrape_queue.pop()
        size_before_scrape = len(scrape_queue)

        schedule = ScheduleParser(urljoin(conf.URL, f'station.php?nnst={station}')).parse()
        for item in schedule:
            train = TrainParser(urljoin(conf.URL, item.url)).parse()
            ignored_stations = set(map(lambda x: x.station_id, train.stations))
            scrape_queue -= ignored_stations

            _log.info(f'removing {len(ignored_stations)} from queue, {len(scrape_queue)} left')

            collection = db.get_collection('trains')
            train.stations = [vars(s) for s in train.stations]
            doc = vars(train)
            collection.replace_one({'_id': doc['_id']}, doc, upsert=True)

            print(train)


# get all stations
# parse a random station
#   get first and last station as endpoints
# parse trains at both endpoints
#   find other endpoint
# do not parse an endpoint twice
def update_trains():
    stations = db.get_collection('stations')
    scrape_queue = set()
    for station_dict in stations.find():
        station = Station(**station_dict)
        scrape_queue.add(station._id)

    _log.info(f'total stations: {len(scrape_queue)}')

    endpoints = set()
    parsed_endpoints = set()
    while True: # TODO: condition
        ...


# @onerror(ret=set())
def get_endpoints(train: Train):
    s = train.stations
    return {s[0].station_id, s[-1].station_id}


def run():
    # update_stations()
    update_trains()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    db.init(conf.DATABASE_CONNECTION)
    run()
