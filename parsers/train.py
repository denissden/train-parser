from models import *
import re
from urllib.parse import parse_qs
from datetime import date, time, datetime
from contextlib import suppress

from utils import onerror
from .base import Parser, strip_time


class TrainParser(Parser):
    @onerror(Exception, warning='failed parsing train')
    def _parse_internal(self):
        title = self.p.find('div', {'class': 'sched_title'})
        title_str = title.text
        number_re = re.compile(f'([0-9]+)')
        number = int(number_re.findall(title_str)[0])

        train = Train(number)
        table_html = self.p.find('table', {'id': 'schedule_table'})
        if table_html is None:
            return
        trs = table_html.find_all('tr')
        for tr in trs:
            with suppress(AttributeError):
                if link := self.parse_tr(tr):
                    train.stations.append(link)

        return train

    @onerror(Exception, warning='failed parsing <tr> in train')
    def parse_tr(self, tr):
        if tds := tr.find_all('td'):
            st_a = tr.find('a')
            q = st_a['href'].split('?')[-1]
            st_number_srt = parse_qs(q)['nnst'][0]
            st_number = int(st_number_srt)
            st_time_str = strip_time(tds[-1].text)

            # if train doesn't stop on the station time is null
            st_datetime = None
            if st_time_str:
                st_time = time.fromisoformat(st_time_str)
                empty_date = date.min
                st_datetime = datetime.combine(empty_date, st_time)

            return StationLink(st_number,
                               st_datetime,
                               stop=st_datetime is not None)
