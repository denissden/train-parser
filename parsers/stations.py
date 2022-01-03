import logging
import re
from models import *
from dataclasses import dataclass

from utils import onerror
from .base import Parser


class StationsParser(Parser):
    zone = -1

    def _parse_internal(self):
        table_html = self.p.find('div', {'id': 'scheme_table'})
        if table_html is None:
            logging.warning(f'did not find table at {self.url}')
            return

        table_contents = table_html.div
        self.zone = -1
        for row_div in table_contents.find_all('div', {'class': ['zone', 'zoneOdd']}):
            # zone is stored in the <p> inside the row div
            zone_info = row_div.find('p', {'class': 'zoneNumber'})
            if zone_info is not None and (text := zone_info.text):
                self.zone = int(text)

            # only yields column if it has a station
            row = row_div.find('div', {'class': 'row'})
            for col_div in row.find_all('div', {'class': 'col'}):
                if col := self.process_col(col_div):
                    yield col

    @onerror(Exception, warning=f'failed parsing col in stations')
    def process_col(self, col):
        if not self.valid_col(col):
            return None

        classes = col['class']
        station_re = re.compile('station.{0,4}')

        if any(re.fullmatch(station_re, c) for c in classes):
            name_a = col.find('a', {'class': 'station-name'})
            name = name_a.text.strip()

            # there are two ways to obtain station number
            number = int(col['id'])
            # href = name_a['href']
            # number = int(href.split('nnst=')[-1])

            metro_a = col.find('a', {'class': 'my_metro'})
            metro = metro_a['title'] != ''

            # TODO: detect subways
            return Station(number,
                           name,
                           zone=self.zone,
                           metro=metro)


        # paths are not needed right now
        # if 'path' in classes:
        #     return Path()

    @staticmethod
    def valid_col(div):
        inner = div['class']
        return len(inner) > 1


class EndRow:
    pass


@dataclass()
class Path:
    # left, top, right, bottom
    L: bool = False
    T: bool = False
    R: bool = False
    B: bool = False

    @staticmethod
    def horizontal():
        return Path(L=True, R=True)

    @staticmethod
    def vertical():
        return Path(T=True, B=True)