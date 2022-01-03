import logging
import re

from models import *
from datetime import date, time, datetime
from contextlib import suppress

from .base import Parser, strip_time
from utils import onerror


class ScheduleParser(Parser):
    def _parse_internal(self):
        logging.info('parsing schedule at {self.url}')

        table_html = self.p.find('table', {'id': 'schedule_table'})
        if table_html is None:
            return

        trs = table_html.find_all('tr')
        for tr in trs:
            sched = self.parse_tr(tr)
            if sched:
                yield sched

    @onerror(Exception, warning=f'failed parsing <tr> in schedule')
    def parse_tr(self, tr):
        if tds := tr.find_all('td'):
            route_a = tr.find('a')
            s_url = route_a['href']

            time_div = tr.find('td', {'class': 'time_with_warn'})
            time_str = strip_time(time_div.find('div').text)
            if not time_str:
                return
            s_time = time.fromisoformat(time_str)
            empty_date = date.min
            s_datetime = datetime.combine(empty_date, s_time)

            s_period = tds[-1].text.strip()

            s = ScheduleItem(s_url, s_datetime, s_period)
            return s


