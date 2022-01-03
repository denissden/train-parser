from models import Direction
from .base import Parser


class DirectionsParser(Parser):

    def _parse_internal(self):
        directions_table = self.p.find('div', {'class': 'directions'})
        for li in directions_table.find_all('li'):
            href = li.a['href']
            yield Direction(li.a.text, href)
